"""
MMH Core System - Immutable Memory Hash Records

Provides the core MMH record structure and verification system for
immutable scientific data storage with cryptographic integrity.
"""

import hashlib
import json
import time
import hmac
import base64
from datetime import datetime
from typing import Dict, Any, Optional, List, Union
from dataclasses import dataclass, asdict
from pathlib import Path
import pickle
import gzip

@dataclass
class MMHRecord:
    """
    Immutable MMH Record Structure
    
    Contains all data needed for 100% reproducible test recreation
    with cryptographic verification of integrity.
    """
    
    # Core identification
    mmh_id: str
    timestamp: str
    record_type: str  # 'test_result', 'scientific_data', 'agent_wisdom', etc.
    
    # Content data (immutable)
    content_hash: str
    content_data: Dict[str, Any]
    content_size: int
    
    # Cryptographic verification
    signature: str
    verification_hash: str
    chain_hash: str  # Links to previous record for chain integrity
    
    # Metadata
    tags: List[str]
    description: str
    author: str
    version: str
    
    # Scientific context
    domain: str  # 'physics', 'climate', 'biology', etc.
    test_name: Optional[str] = None
    reproducibility_score: Optional[float] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert record to dictionary for storage"""
        return asdict(self)
    
    def to_json(self) -> str:
        """Convert record to JSON string"""
        return json.dumps(self.to_dict(), indent=2, sort_keys=True)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MMHRecord':
        """Create record from dictionary"""
        return cls(**data)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'MMHRecord':
        """Create record from JSON string"""
        return cls.from_dict(json.loads(json_str))


class MMHCore:
    """
    Core MMH System for immutable data storage and verification
    """
    
    def __init__(self, storage_path: str = "mmh_storage"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(exist_ok=True)
        self.chain_file = self.storage_path / "mmh_chain.json"
        self.records_file = self.storage_path / "mmh_records.json"
        
        # Initialize storage
        self._load_chain()
        self._load_records()
    
    def _load_chain(self):
        """Load MMH chain for integrity verification"""
        if self.chain_file.exists():
            with open(self.chain_file, 'r') as f:
                self.chain = json.load(f)
        else:
            self.chain = {"genesis": "GENESIS_BLOCK", "records": []}
            self._save_chain()
    
    def _save_chain(self):
        """Save MMH chain"""
        with open(self.chain_file, 'w') as f:
            json.dump(self.chain, f, indent=2)
    
    def _load_records(self):
        """Load existing MMH records"""
        if self.records_file.exists():
            with open(self.records_file, 'r') as f:
                self.records = json.load(f)
        else:
            self.records = {}
            self._save_records()
    
    def _save_records(self):
        """Save MMH records"""
        with open(self.records_file, 'w') as f:
            json.dump(self.records, f, indent=2)
    
    def create_record(self, 
                     content_data: Dict[str, Any],
                     record_type: str,
                     domain: str,
                     tags: List[str],
                     description: str,
                     author: str,
                     test_name: Optional[str] = None) -> MMHRecord:
        """
        Create a new immutable MMH record
        
        Args:
            content_data: The data to store immutably
            record_type: Type of record ('test_result', 'scientific_data', etc.)
            domain: Scientific domain ('physics', 'climate', etc.)
            tags: Searchable tags
            description: Human-readable description
            author: Record author
            test_name: Associated test name if applicable
            
        Returns:
            MMHRecord: Immutable record with cryptographic verification
        """
        
        # Generate unique MMH ID
        timestamp = datetime.utcnow().isoformat()
        mmh_id = self._generate_mmh_id(content_data, timestamp)
        
        # Compress and hash content
        compressed_content = self._compress_content(content_data)
        content_hash = self._hash_content(compressed_content)
        
        # Create signature
        signature = self._create_signature(content_hash, timestamp)
        
        # Generate verification hash
        verification_hash = self._create_verification_hash(
            mmh_id, content_hash, signature, timestamp
        )
        
        # Link to previous record for chain integrity
        chain_hash = self._get_chain_hash()
        
        # Create record
        record = MMHRecord(
            mmh_id=mmh_id,
            timestamp=timestamp,
            record_type=record_type,
            content_hash=content_hash,
            content_data=content_data,
            content_size=len(compressed_content),
            signature=signature,
            verification_hash=verification_hash,
            chain_hash=chain_hash,
            tags=tags,
            description=description,
            author=author,
            version="1.0.0",
            domain=domain,
            test_name=test_name,
            reproducibility_score=self._calculate_reproducibility_score(content_data)
        )
        
        # Store record
        self._store_record(record)
        
        return record
    
    def _generate_mmh_id(self, content_data: Dict[str, Any], timestamp: str) -> str:
        """Generate unique MMH ID"""
        content_str = json.dumps(content_data, sort_keys=True)
        hash_input = f"{content_str}{timestamp}{len(self.records)}"
        return hashlib.sha256(hash_input.encode()).hexdigest()[:16]
    
    def _compress_content(self, content_data: Dict[str, Any]) -> bytes:
        """Compress content data"""
        content_str = json.dumps(content_data, sort_keys=True)
        return gzip.compress(content_str.encode())
    
    def _hash_content(self, compressed_content: bytes) -> str:
        """Hash compressed content"""
        return hashlib.sha256(compressed_content).hexdigest()
    
    def _create_signature(self, content_hash: str, timestamp: str) -> str:
        """Create cryptographic signature"""
        signature_data = f"{content_hash}{timestamp}"
        return hmac.new(
            b"kai_core_mmh_secret",  # In production, use proper key management
            signature_data.encode(),
            hashlib.sha256
        ).hexdigest()
    
    def _create_verification_hash(self, mmh_id: str, content_hash: str, 
                                signature: str, timestamp: str) -> str:
        """Create verification hash for integrity checking"""
        verification_data = f"{mmh_id}{content_hash}{signature}{timestamp}"
        return hashlib.sha256(verification_data.encode()).hexdigest()
    
    def _get_chain_hash(self) -> str:
        """Get hash of previous record for chain integrity"""
        if not self.chain["records"]:
            return "GENESIS"
        return self.chain["records"][-1]["verification_hash"]
    
    def _calculate_reproducibility_score(self, content_data: Dict[str, Any]) -> float:
        """Calculate reproducibility score based on content completeness"""
        score = 0.0
        
        # Check for essential reproducibility elements
        if "test_name" in content_data:
            score += 0.2
        if "input_data" in content_data:
            score += 0.3
        if "parameters" in content_data:
            score += 0.2
        if "results" in content_data:
            score += 0.2
        if "environment" in content_data:
            score += 0.1
            
        return min(score, 1.0)
    
    def _store_record(self, record: MMHRecord):
        """Store record in MMH system"""
        # Add to records
        self.records[record.mmh_id] = record.to_dict()
        
        # Add to chain
        self.chain["records"].append({
            "mmh_id": record.mmh_id,
            "timestamp": record.timestamp,
            "verification_hash": record.verification_hash
        })
        
        # Save to storage
        self._save_records()
        self._save_chain()
    
    def get_record(self, mmh_id: str) -> Optional[MMHRecord]:
        """Retrieve MMH record by ID"""
        if mmh_id in self.records:
            return MMHRecord.from_dict(self.records[mmh_id])
        return None
    
    def verify_record(self, record: MMHRecord) -> bool:
        """Verify MMH record integrity"""
        try:
            # Verify content hash
            compressed_content = self._compress_content(record.content_data)
            expected_hash = self._hash_content(compressed_content)
            if record.content_hash != expected_hash:
                return False
            
            # Verify signature
            expected_signature = self._create_signature(
                record.content_hash, record.timestamp
            )
            if record.signature != expected_signature:
                return False
            
            # Verify verification hash
            expected_verification = self._create_verification_hash(
                record.mmh_id, record.content_hash, 
                record.signature, record.timestamp
            )
            if record.verification_hash != expected_verification:
                return False
            
            return True
            
        except Exception:
            return False
    
    def search_records(self, 
                      tags: Optional[List[str]] = None,
                      domain: Optional[str] = None,
                      record_type: Optional[str] = None,
                      author: Optional[str] = None) -> List[MMHRecord]:
        """Search MMH records by criteria"""
        results = []
        
        for record_dict in self.records.values():
            record = MMHRecord.from_dict(record_dict)
            
            # Apply filters
            if tags and not any(tag in record.tags for tag in tags):
                continue
            if domain and record.domain != domain:
                continue
            if record_type and record.record_type != record_type:
                continue
            if author and record.author != author:
                continue
                
            results.append(record)
        
        return results
    
    def get_chain_integrity(self) -> Dict[str, Any]:
        """Check MMH chain integrity"""
        integrity_report = {
            "total_records": len(self.chain["records"]),
            "chain_verified": True,
            "broken_links": [],
            "verification_errors": []
        }
        
        for i, record_info in enumerate(self.chain["records"]):
            mmh_id = record_info["mmh_id"]
            record = self.get_record(mmh_id)
            
            if not record:
                integrity_report["broken_links"].append(mmh_id)
                integrity_report["chain_verified"] = False
                continue
            
            if not self.verify_record(record):
                integrity_report["verification_errors"].append(mmh_id)
                integrity_report["chain_verified"] = False
        
        return integrity_report


class MMHVerifier:
    """
    MMH Verification System for integrity checking
    """
    
    def __init__(self, mmh_core: MMHCore):
        self.mmh_core = mmh_core
    
    def verify_record_integrity(self, mmh_id: str) -> Dict[str, Any]:
        """Verify integrity of specific MMH record"""
        record = self.mmh_core.get_record(mmh_id)
        
        if not record:
            return {
                "mmh_id": mmh_id,
                "exists": False,
                "integrity_verified": False,
                "error": "Record not found"
            }
        
        integrity_verified = self.mmh_core.verify_record(record)
        
        return {
            "mmh_id": mmh_id,
            "exists": True,
            "integrity_verified": integrity_verified,
            "record_type": record.record_type,
            "domain": record.domain,
            "timestamp": record.timestamp,
            "reproducibility_score": record.reproducibility_score
        }
    
    def verify_chain_integrity(self) -> Dict[str, Any]:
        """Verify entire MMH chain integrity"""
        return self.mmh_core.get_chain_integrity()
    
    def verify_reproducibility(self, mmh_id: str) -> Dict[str, Any]:
        """Verify if record contains all data needed for reproduction"""
        record = self.mmh_core.get_record(mmh_id)
        
        if not record:
            return {
                "mmh_id": mmh_id,
                "reproducible": False,
                "error": "Record not found"
            }
        
        # Check for essential reproducibility elements
        content = record.content_data
        required_elements = ["test_name", "input_data", "parameters", "results"]
        missing_elements = [elem for elem in required_elements if elem not in content]
        
        return {
            "mmh_id": mmh_id,
            "reproducible": len(missing_elements) == 0,
            "reproducibility_score": record.reproducibility_score,
            "missing_elements": missing_elements,
            "has_environment": "environment" in content
        } 