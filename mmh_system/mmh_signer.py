"""
MMH Signer System

Provides cryptographic signing and validation for MMH records
to ensure data integrity and authenticity.
"""

import hashlib
import hmac
import base64
import json
from datetime import datetime
from typing import Dict, Any, Optional, List
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, NoEncryption

from .mmh_core import MMHRecord


class MMHSigner:
    """
    Cryptographic signer for MMH records
    """
    
    def __init__(self, private_key_path: Optional[str] = None):
        self.private_key_path = private_key_path
        self.private_key = None
        self.public_key = None
        
        if private_key_path:
            self._load_keys()
        else:
            self._generate_keys()
    
    def _generate_keys(self):
        """Generate RSA key pair for signing"""
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        self.public_key = self.private_key.public_key()
    
    def _load_keys(self):
        """Load existing RSA keys"""
        try:
            with open(self.private_key_path, 'rb') as f:
                self.private_key = rsa.load_private_key(f.read())
            self.public_key = self.private_key.public_key()
        except Exception as e:
            print(f"Warning: Could not load keys from {self.private_key_path}: {e}")
            self._generate_keys()
    
    def sign_record(self, record: MMHRecord) -> str:
        """Sign MMH record with RSA private key"""
        # Create signature data
        signature_data = {
            "mmh_id": record.mmh_id,
            "content_hash": record.content_hash,
            "timestamp": record.timestamp,
            "record_type": record.record_type,
            "domain": record.domain
        }
        
        signature_str = json.dumps(signature_data, sort_keys=True)
        
        # Sign with private key
        signature = self.private_key.sign(
            signature_str.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        
        return base64.b64encode(signature).decode()
    
    def verify_signature(self, record: MMHRecord, signature: str) -> bool:
        """Verify MMH record signature with public key"""
        try:
            # Recreate signature data
            signature_data = {
                "mmh_id": record.mmh_id,
                "content_hash": record.content_hash,
                "timestamp": record.timestamp,
                "record_type": record.record_type,
                "domain": record.domain
            }
            
            signature_str = json.dumps(signature_data, sort_keys=True)
            
            # Decode signature
            signature_bytes = base64.b64decode(signature)
            
            # Verify with public key
            self.public_key.verify(
                signature_bytes,
                signature_str.encode(),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            
            return True
            
        except Exception:
            return False
    
    def export_public_key(self) -> str:
        """Export public key for verification"""
        pem = self.public_key.public_bytes(
            encoding=Encoding.PEM,
            format=PrivateFormat.PKCS8
        )
        return pem.decode()
    
    def save_keys(self, private_key_path: str, public_key_path: str):
        """Save RSA keys to files"""
        # Save private key
        with open(private_key_path, 'wb') as f:
            f.write(self.private_key.private_bytes(
                encoding=Encoding.PEM,
                format=PrivateFormat.PKCS8,
                encryption_algorithm=NoEncryption()
            ))
        
        # Save public key
        with open(public_key_path, 'wb') as f:
            f.write(self.public_key.public_bytes(
                encoding=Encoding.PEM,
                format=PrivateFormat.SubjectPublicKeyInfo
            ))


class MMHValidator:
    """
    MMH record validator for integrity and authenticity verification
    """
    
    def __init__(self, signer: MMHSigner):
        self.signer = signer
    
    def validate_record(self, record: MMHRecord) -> Dict[str, Any]:
        """Comprehensive validation of MMH record"""
        validation_result = {
            "mmh_id": record.mmh_id,
            "timestamp": record.timestamp,
            "validation_passed": True,
            "errors": [],
            "warnings": []
        }
        
        # Check basic structure
        if not self._validate_structure(record):
            validation_result["validation_passed"] = False
            validation_result["errors"].append("Invalid record structure")
        
        # Check content integrity
        if not self._validate_content_integrity(record):
            validation_result["validation_passed"] = False
            validation_result["errors"].append("Content integrity check failed")
        
        # Check cryptographic signature
        if not self._validate_signature(record):
            validation_result["validation_passed"] = False
            validation_result["errors"].append("Cryptographic signature verification failed")
        
        # Check chain integrity
        if not self._validate_chain_integrity(record):
            validation_result["warnings"].append("Chain integrity warning")
        
        # Check reproducibility
        reproducibility_check = self._validate_reproducibility(record)
        validation_result["reproducibility"] = reproducibility_check
        
        return validation_result
    
    def _validate_structure(self, record: MMHRecord) -> bool:
        """Validate MMH record structure"""
        required_fields = [
            'mmh_id', 'timestamp', 'record_type', 'domain',
            'content_hash', 'content_data', 'content_size',
            'signature', 'verification_hash', 'chain_hash',
            'tags', 'description', 'author', 'version'
        ]
        
        for field in required_fields:
            if not hasattr(record, field) or getattr(record, field) is None:
                return False
        
        return True
    
    def _validate_content_integrity(self, record: MMHRecord) -> bool:
        """Validate content hash integrity"""
        try:
            import gzip
            content_str = json.dumps(record.content_data, sort_keys=True)
            compressed_content = gzip.compress(content_str.encode())
            expected_hash = hashlib.sha256(compressed_content).hexdigest()
            
            return record.content_hash == expected_hash
            
        except Exception:
            return False
    
    def _validate_signature(self, record: MMHRecord) -> bool:
        """Validate cryptographic signature"""
        return self.signer.verify_signature(record, record.signature)
    
    def _validate_chain_integrity(self, record: MMHRecord) -> bool:
        """Validate chain integrity (basic check)"""
        # This would need access to the full chain for complete validation
        # For now, just check that chain_hash is present
        return bool(record.chain_hash)
    
    def _validate_reproducibility(self, record: MMHRecord) -> Dict[str, Any]:
        """Validate reproducibility requirements"""
        content = record.content_data
        required_elements = ["test_name", "input_data", "parameters", "results"]
        optional_elements = ["environment", "dependencies", "random_seed"]
        
        missing_required = [elem for elem in required_elements if elem not in content]
        missing_optional = [elem for elem in optional_elements if elem not in content]
        
        return {
            "reproducible": len(missing_required) == 0,
            "missing_required": missing_required,
            "missing_optional": missing_optional,
            "reproducibility_score": record.reproducibility_score,
            "has_environment": "environment" in content,
            "has_dependencies": "dependencies" in content,
            "has_random_seed": "random_seed" in content
        }
    
    def validate_batch(self, records: List[MMHRecord]) -> Dict[str, Any]:
        """Validate multiple MMH records"""
        batch_result = {
            "total_records": len(records),
            "valid_records": 0,
            "invalid_records": 0,
            "reproducible_records": 0,
            "validation_results": []
        }
        
        for record in records:
            validation = self.validate_record(record)
            batch_result["validation_results"].append(validation)
            
            if validation["validation_passed"]:
                batch_result["valid_records"] += 1
            else:
                batch_result["invalid_records"] += 1
            
            if validation.get("reproducibility", {}).get("reproducible", False):
                batch_result["reproducible_records"] += 1
        
        return batch_result
    
    def generate_validation_report(self, records: List[MMHRecord]) -> str:
        """Generate detailed validation report"""
        batch_result = self.validate_batch(records)
        
        report = []
        report.append("# MMH Validation Report")
        report.append(f"Generated: {datetime.utcnow().isoformat()}")
        report.append("")
        
        report.append("## Summary")
        report.append(f"- Total Records: {batch_result['total_records']}")
        report.append(f"- Valid Records: {batch_result['valid_records']}")
        report.append(f"- Invalid Records: {batch_result['invalid_records']}")
        report.append(f"- Reproducible Records: {batch_result['reproducible_records']}")
        report.append("")
        
        report.append("## Detailed Results")
        for i, validation in enumerate(batch_result["validation_results"]):
            report.append(f"### Record {i+1}: {validation['mmh_id']}")
            report.append(f"- Timestamp: {validation['timestamp']}")
            report.append(f"- Validation: {'✅ PASSED' if validation['validation_passed'] else '❌ FAILED'}")
            
            if validation["errors"]:
                report.append(f"- Errors: {', '.join(validation['errors'])}")
            
            if validation["warnings"]:
                report.append(f"- Warnings: {', '.join(validation['warnings'])}")
            
            reproducibility = validation.get("reproducibility", {})
            report.append(f"- Reproducible: {'✅ YES' if reproducibility.get('reproducible') else '❌ NO'}")
            report.append(f"- Reproducibility Score: {reproducibility.get('reproducibility_score', 'N/A')}")
            report.append("")
        
        return "\n".join(report) 