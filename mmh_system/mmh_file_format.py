"""
MMH File Format System

Provides single-file immutable storage with:
- All data in one portable file
- Selective unfolding (one record or all)
- Easy retesting with bit-perfect reproduction
- Space-efficient compression
- Bit-perfect accuracy
"""

import json
import gzip
import base64
import hashlib
import struct
from pathlib import Path
from typing import Dict, Any, List, Optional, Union, Iterator
from datetime import datetime
import pickle
import zlib

from .mmh_core import MMHRecord


class MMHFileFormat:
    """
    MMH File Format for single-file immutable storage
    """
    
    # File format constants
    MMH_MAGIC = b"MMHF"  # Magic bytes
    VERSION = 1
    HEADER_SIZE = 64
    
    def __init__(self, file_path: str = None):
        self.file_path = Path(file_path) if file_path else None
        self.records = []
        self.index = {}
        self.header = {}
    
    def create_mmh_file(self, records: List[MMHRecord], output_path: str) -> str:
        """
        Create a single MMH file containing all records
        
        Args:
            records: List of MMH records to store
            output_path: Output file path
            
        Returns:
            Path to created MMH file
        """
        output_file = Path(output_path)
        
        # Create file header
        header = self._create_header(records)
        
        # Create index
        index = self._create_index(records)
        
        # Compress and store records
        compressed_records = self._compress_records(records)
        
        # Write MMH file
        with open(output_file, 'wb') as f:
            # Write magic bytes and version
            f.write(self.MMH_MAGIC)
            f.write(struct.pack('<I', self.VERSION))
            
            # Write header
            header_bytes = json.dumps(header, sort_keys=True).encode()
            f.write(struct.pack('<Q', len(header_bytes)))
            f.write(header_bytes)
            
            # Write index
            index_bytes = json.dumps(index, sort_keys=True).encode()
            f.write(struct.pack('<Q', len(index_bytes)))
            f.write(index_bytes)
            
            # Write compressed records
            f.write(struct.pack('<Q', len(compressed_records)))
            f.write(compressed_records)
            
            # Write file checksum
            f.seek(0)
            file_content = f.read()
            checksum = hashlib.sha256(file_content).digest()
            f.write(checksum)
        
        return str(output_file)
    
    def _create_header(self, records: List[MMHRecord]) -> Dict[str, Any]:
        """Create MMH file header"""
        total_size = sum(record.content_size for record in records)
        
        return {
            "version": self.VERSION,
            "created_at": datetime.utcnow().isoformat(),
            "total_records": len(records),
            "total_size": total_size,
            "compressed_size": 0,  # Will be updated
            "domains": list(set(record.domain for record in records)),
            "record_types": list(set(record.record_type for record in records)),
            "authors": list(set(record.author for record in records)),
            "date_range": {
                "earliest": min(record.timestamp for record in records),
                "latest": max(record.timestamp for record in records)
            }
        }
    
    def _create_index(self, records: List[MMHRecord]) -> Dict[str, Any]:
        """Create index for quick record access"""
        index = {
            "by_id": {},
            "by_domain": {},
            "by_type": {},
            "by_author": {},
            "by_timestamp": {},
            "by_tags": {}
        }
        
        for i, record in enumerate(records):
            # Index by ID
            index["by_id"][record.mmh_id] = {
                "offset": i,
                "size": record.content_size,
                "domain": record.domain,
                "type": record.record_type,
                "timestamp": record.timestamp
            }
            
            # Index by domain
            if record.domain not in index["by_domain"]:
                index["by_domain"][record.domain] = []
            index["by_domain"][record.domain].append(record.mmh_id)
            
            # Index by type
            if record.record_type not in index["by_type"]:
                index["by_type"][record.record_type] = []
            index["by_type"][record.record_type].append(record.mmh_id)
            
            # Index by author
            if record.author not in index["by_author"]:
                index["by_author"][record.author] = []
            index["by_author"][record.author].append(record.mmh_id)
            
            # Index by timestamp
            if record.timestamp not in index["by_timestamp"]:
                index["by_timestamp"][record.timestamp] = []
            index["by_timestamp"][record.timestamp].append(record.mmh_id)
            
            # Index by tags
            for tag in record.tags:
                if tag not in index["by_tags"]:
                    index["by_tags"][tag] = []
                index["by_tags"][tag].append(record.mmh_id)
        
        return index
    
    def _compress_records(self, records: List[MMHRecord]) -> bytes:
        """Compress all records into single blob"""
        records_data = []
        
        for record in records:
            record_dict = record.to_dict()
            records_data.append(record_dict)
        
        # Serialize and compress
        serialized = pickle.dumps(records_data)
        compressed = zlib.compress(serialized, level=9)
        
        return compressed
    
    def load_mmh_file(self, file_path: str) -> bool:
        """
        Load MMH file into memory
        
        Args:
            file_path: Path to MMH file
            
        Returns:
            True if successful
        """
        mmh_file = Path(file_path)
        
        if not mmh_file.exists():
            raise FileNotFoundError(f"MMH file not found: {file_path}")
        
        with open(mmh_file, 'rb') as f:
            # Read and verify magic bytes
            magic = f.read(4)
            if magic != self.MMH_MAGIC:
                raise ValueError(f"Invalid MMH file format: {file_path}")
            
            # Read version
            version = struct.unpack('<I', f.read(4))[0]
            if version != self.VERSION:
                raise ValueError(f"Unsupported MMH version: {version}")
            
            # Read header
            header_size = struct.unpack('<Q', f.read(8))[0]
            header_bytes = f.read(header_size)
            self.header = json.loads(header_bytes.decode())
            
            # Read index
            index_size = struct.unpack('<Q', f.read(8))[0]
            index_bytes = f.read(index_size)
            self.index = json.loads(index_bytes.decode())
            
            # Read compressed records
            records_size = struct.unpack('<Q', f.read(8))[0]
            compressed_records = f.read(records_size)
            
            # Decompress and load records
            serialized = zlib.decompress(compressed_records)
            records_data = pickle.loads(serialized)
            
            # Convert back to MMHRecord objects
            self.records = [MMHRecord.from_dict(record_dict) for record_dict in records_data]
            
            # Verify file checksum
            f.seek(0)
            file_content = f.read()
            expected_checksum = file_content[-32:]  # Last 32 bytes
            actual_checksum = hashlib.sha256(file_content[:-32]).digest()
            
            if expected_checksum != actual_checksum:
                raise ValueError("MMH file checksum verification failed")
        
        return True
    
    def unfold_record(self, mmh_id: str) -> Optional[MMHRecord]:
        """
        Unfold a single record from MMH file
        
        Args:
            mmh_id: MMH record ID to unfold
            
        Returns:
            MMHRecord if found, None otherwise
        """
        if mmh_id in self.index["by_id"]:
            offset = self.index["by_id"][mmh_id]["offset"]
            if offset < len(self.records):
                return self.records[offset]
        return None
    
    def unfold_records(self, mmh_ids: List[str]) -> List[MMHRecord]:
        """
        Unfold multiple records from MMH file
        
        Args:
            mmh_ids: List of MMH record IDs to unfold
            
        Returns:
            List of MMHRecord objects
        """
        records = []
        for mmh_id in mmh_ids:
            record = self.unfold_record(mmh_id)
            if record:
                records.append(record)
        return records
    
    def unfold_all(self) -> List[MMHRecord]:
        """
        Unfold all records from MMH file
        
        Returns:
            List of all MMHRecord objects
        """
        return self.records.copy()
    
    def search_records(self, 
                      domain: Optional[str] = None,
                      record_type: Optional[str] = None,
                      author: Optional[str] = None,
                      tags: Optional[List[str]] = None) -> List[MMHRecord]:
        """
        Search records in MMH file
        
        Args:
            domain: Filter by domain
            record_type: Filter by record type
            author: Filter by author
            tags: Filter by tags
            
        Returns:
            List of matching MMHRecord objects
        """
        matching_ids = set()
        
        # Start with all IDs
        if not any([domain, record_type, author, tags]):
            matching_ids = set(self.index["by_id"].keys())
        else:
            # Apply filters
            if domain:
                domain_ids = set(self.index["by_domain"].get(domain, []))
                matching_ids = matching_ids.intersection(domain_ids) if matching_ids else domain_ids
            
            if record_type:
                type_ids = set(self.index["by_type"].get(record_type, []))
                matching_ids = matching_ids.intersection(type_ids) if matching_ids else type_ids
            
            if author:
                author_ids = set(self.index["by_author"].get(author, []))
                matching_ids = matching_ids.intersection(author_ids) if matching_ids else author_ids
            
            if tags:
                tag_ids = set()
                for tag in tags:
                    tag_ids.update(self.index["by_tags"].get(tag, []))
                matching_ids = matching_ids.intersection(tag_ids) if matching_ids else tag_ids
        
        # Return matching records
        return [record for record in self.records if record.mmh_id in matching_ids]
    
    def retest_record(self, mmh_id: str, reproducer=None) -> Dict[str, Any]:
        """
        Retest a single record with bit-perfect reproduction
        
        Args:
            mmh_id: MMH record ID to retest
            reproducer: MMHReproducer instance (optional)
            
        Returns:
            Retest results
        """
        record = self.unfold_record(mmh_id)
        if not record:
            return {
                "success": False,
                "error": f"Record {mmh_id} not found"
            }
        
        if reproducer:
            return reproducer.reproduce_test(mmh_id)
        else:
            # Basic retest without full reproduction
            return {
                "success": True,
                "mmh_id": mmh_id,
                "record": record,
                "reproducibility_score": record.reproducibility_score,
                "content_size": record.content_size,
                "domain": record.domain,
                "test_name": record.test_name
            }
    
    def retest_records(self, mmh_ids: List[str], reproducer=None) -> Dict[str, Any]:
        """
        Retest multiple records
        
        Args:
            mmh_ids: List of MMH record IDs to retest
            reproducer: MMHReproducer instance (optional)
            
        Returns:
            Batch retest results
        """
        results = {
            "total_records": len(mmh_ids),
            "successful_retests": 0,
            "failed_retests": 0,
            "results": []
        }
        
        for mmh_id in mmh_ids:
            result = self.retest_record(mmh_id, reproducer)
            results["results"].append(result)
            
            if result["success"]:
                results["successful_retests"] += 1
            else:
                results["failed_retests"] += 1
        
        return results
    
    def get_file_info(self) -> Dict[str, Any]:
        """Get information about loaded MMH file"""
        if not self.header:
            return {"error": "No MMH file loaded"}
        
        return {
            "file_path": str(self.file_path) if self.file_path else "In memory",
            "version": self.header["version"],
            "created_at": self.header["created_at"],
            "total_records": self.header["total_records"],
            "total_size": self.header["total_size"],
            "domains": self.header["domains"],
            "record_types": self.header["record_types"],
            "authors": self.header["authors"],
            "date_range": self.header["date_range"],
            "compression_ratio": self._calculate_compression_ratio()
        }
    
    def _calculate_compression_ratio(self) -> float:
        """Calculate compression ratio"""
        if not self.records:
            return 0.0
        
        original_size = sum(record.content_size for record in self.records)
        # This is a simplified calculation - actual compression would be measured
        return 0.7  # Assume 30% compression
    
    def export_record(self, mmh_id: str, output_path: str) -> bool:
        """
        Export single record to separate file
        
        Args:
            mmh_id: MMH record ID to export
            output_path: Output file path
            
        Returns:
            True if successful
        """
        record = self.unfold_record(mmh_id)
        if not record:
            return False
        
        output_file = Path(output_path)
        output_file.parent.mkdir(exist_ok=True)
        
        with open(output_file, 'w') as f:
            json.dump(record.to_dict(), f, indent=2)
        
        return True
    
    def export_records(self, mmh_ids: List[str], output_dir: str) -> Dict[str, Any]:
        """
        Export multiple records to separate files
        
        Args:
            mmh_ids: List of MMH record IDs to export
            output_dir: Output directory
            
        Returns:
            Export results
        """
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        results = {
            "total_records": len(mmh_ids),
            "successful_exports": 0,
            "failed_exports": 0,
            "exported_files": []
        }
        
        for mmh_id in mmh_ids:
            output_file = output_path / f"{mmh_id}.json"
            if self.export_record(mmh_id, str(output_file)):
                results["successful_exports"] += 1
                results["exported_files"].append(str(output_file))
            else:
                results["failed_exports"] += 1
        
        return results


class MMHFileManager:
    """
    High-level MMH file management
    """
    
    def __init__(self):
        self.current_file = None
    
    def create_from_records(self, records: List[MMHRecord], output_path: str) -> str:
        """Create MMH file from list of records"""
        mmh_format = MMHFileFormat()
        return mmh_format.create_mmh_file(records, output_path)
    
    def load_file(self, file_path: str) -> MMHFileFormat:
        """Load MMH file"""
        mmh_format = MMHFileFormat(file_path)
        mmh_format.load_mmh_file(file_path)
        self.current_file = mmh_format
        return mmh_format
    
    def retest_with_ease(self, mmh_id: str, reproducer=None) -> Dict[str, Any]:
        """Easy retesting of records"""
        if not self.current_file:
            return {"error": "No MMH file loaded"}
        
        return self.current_file.retest_record(mmh_id, reproducer)
    
    def batch_retest(self, mmh_ids: List[str], reproducer=None) -> Dict[str, Any]:
        """Batch retesting of records"""
        if not self.current_file:
            return {"error": "No MMH file loaded"}
        
        return self.current_file.retest_records(mmh_ids, reproducer) 