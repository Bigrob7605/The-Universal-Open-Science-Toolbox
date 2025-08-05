"""
Simple MMH File Format

Basic single-file storage for MMH records
"""

import json
import hashlib
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

from .mmh_core import MMHRecord


class SimpleMMHFile:
    """
    Simple MMH file format for single-file storage
    """
    
    def __init__(self):
        self.records = []
        self.index = {}
        self.header = {}
    
    def create_simple_mmh_file(self, records: List[MMHRecord], output_path: str) -> str:
        """
        Create a simple MMH file containing all records
        
        Args:
            records: List of MMH records to store
            output_path: Output file path
            
        Returns:
            Path to created MMH file
        """
        output_file = Path(output_path)
        
        # Create file data
        file_data = {
            "magic": "MMHF",
            "version": 1,
            "created_at": datetime.utcnow().isoformat(),
            "total_records": len(records),
            "records": [record.to_dict() for record in records],
            "index": self._create_simple_index(records),
            "checksum": self._calculate_checksum(records)
        }
        
        # Write file
        with open(output_file, 'w') as f:
            json.dump(file_data, f, indent=2)
        
        return str(output_file)
    
    def _create_simple_index(self, records: List[MMHRecord]) -> Dict[str, Any]:
        """Create simple index"""
        index = {
            "by_id": {},
            "by_domain": {},
            "by_type": {}
        }
        
        for i, record in enumerate(records):
            # Index by ID
            index["by_id"][record.mmh_id] = {
                "offset": i,
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
        
        return index
    
    def _calculate_checksum(self, records: List[MMHRecord]) -> str:
        """Calculate checksum of records"""
        data_str = json.dumps([record.to_dict() for record in records], sort_keys=True)
        return hashlib.sha256(data_str.encode()).hexdigest()
    
    def load_simple_mmh_file(self, file_path: str) -> bool:
        """
        Load simple MMH file
        
        Args:
            file_path: Path to MMH file
            
        Returns:
            True if successful
        """
        mmh_file = Path(file_path)
        
        if not mmh_file.exists():
            raise FileNotFoundError(f"MMH file not found: {file_path}")
        
        with open(mmh_file, 'r') as f:
            file_data = json.load(f)
        
        # Verify magic
        if file_data.get("magic") != "MMHF":
            raise ValueError(f"Invalid MMH file format: {file_path}")
        
        # Load data
        self.header = {
            "version": file_data["version"],
            "created_at": file_data["created_at"],
            "total_records": file_data["total_records"]
        }
        
        self.index = file_data["index"]
        
        # Convert records
        self.records = [MMHRecord.from_dict(record_dict) for record_dict in file_data["records"]]
        
        # Verify checksum
        expected_checksum = file_data["checksum"]
        actual_checksum = self._calculate_checksum(self.records)
        
        if expected_checksum != actual_checksum:
            raise ValueError("MMH file checksum verification failed")
        
        return True
    
    def unfold_record(self, mmh_id: str) -> Optional[MMHRecord]:
        """Unfold a single record"""
        if mmh_id in self.index["by_id"]:
            offset = self.index["by_id"][mmh_id]["offset"]
            if offset < len(self.records):
                return self.records[offset]
        return None
    
    def unfold_all(self) -> List[MMHRecord]:
        """Unfold all records"""
        return self.records.copy()
    
    def search_records(self, domain: Optional[str] = None) -> List[MMHRecord]:
        """Search records by domain"""
        if not domain:
            return self.records.copy()
        
        domain_ids = self.index["by_domain"].get(domain, [])
        return [record for record in self.records if record.mmh_id in domain_ids]
    
    def retest_record(self, mmh_id: str) -> Dict[str, Any]:
        """Retest a single record"""
        record = self.unfold_record(mmh_id)
        if not record:
            return {
                "success": False,
                "error": f"Record {mmh_id} not found"
            }
        
        return {
            "success": True,
            "mmh_id": mmh_id,
            "reproducibility_score": record.reproducibility_score,
            "content_size": record.content_size,
            "domain": record.domain,
            "test_name": record.test_name
        }
    
    def get_file_info(self) -> Dict[str, Any]:
        """Get file information"""
        if not self.header:
            return {"error": "No MMH file loaded"}
        
        return {
            "version": self.header["version"],
            "created_at": self.header["created_at"],
            "total_records": self.header["total_records"],
            "domains": list(self.index["by_domain"].keys()),
            "record_types": list(self.index["by_type"].keys())
        } 