"""
MMH Storage System

Provides database and file-based storage for MMH records with
efficient querying and backup capabilities.
"""

import sqlite3
import json
import pickle
import gzip
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
import shutil
import hashlib

from .mmh_core import MMHRecord


class MMHDatabase:
    """
    SQLite database for MMH record storage and querying
    """
    
    def __init__(self, db_path: str = "mmh_storage/mmh.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(exist_ok=True)
        self._init_database()
    
    def _init_database(self):
        """Initialize MMH database with required tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Create records table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS mmh_records (
                    mmh_id TEXT PRIMARY KEY,
                    timestamp TEXT NOT NULL,
                    record_type TEXT NOT NULL,
                    domain TEXT NOT NULL,
                    content_hash TEXT NOT NULL,
                    content_data TEXT NOT NULL,
                    content_size INTEGER NOT NULL,
                    signature TEXT NOT NULL,
                    verification_hash TEXT NOT NULL,
                    chain_hash TEXT NOT NULL,
                    tags TEXT NOT NULL,
                    description TEXT NOT NULL,
                    author TEXT NOT NULL,
                    version TEXT NOT NULL,
                    test_name TEXT,
                    reproducibility_score REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create indexes for efficient querying
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_record_type 
                ON mmh_records(record_type)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_domain 
                ON mmh_records(domain)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_author 
                ON mmh_records(author)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_timestamp 
                ON mmh_records(timestamp)
            """)
            
            conn.commit()
    
    def store_record(self, record: MMHRecord):
        """Store MMH record in database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO mmh_records (
                    mmh_id, timestamp, record_type, domain, content_hash,
                    content_data, content_size, signature, verification_hash,
                    chain_hash, tags, description, author, version,
                    test_name, reproducibility_score
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                record.mmh_id,
                record.timestamp,
                record.record_type,
                record.domain,
                record.content_hash,
                json.dumps(record.content_data),
                record.content_size,
                record.signature,
                record.verification_hash,
                record.chain_hash,
                json.dumps(record.tags),
                record.description,
                record.author,
                record.version,
                record.test_name,
                record.reproducibility_score
            ))
            
            conn.commit()
    
    def get_record(self, mmh_id: str) -> Optional[MMHRecord]:
        """Retrieve MMH record from database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM mmh_records WHERE mmh_id = ?
            """, (mmh_id,))
            
            row = cursor.fetchone()
            if not row:
                return None
            
            # Reconstruct MMHRecord from database row
            record_dict = {
                "mmh_id": row[0],
                "timestamp": row[1],
                "record_type": row[2],
                "domain": row[3],
                "content_hash": row[4],
                "content_data": json.loads(row[5]),
                "content_size": row[6],
                "signature": row[7],
                "verification_hash": row[8],
                "chain_hash": row[9],
                "tags": json.loads(row[10]),
                "description": row[11],
                "author": row[12],
                "version": row[13],
                "test_name": row[14],
                "reproducibility_score": row[15]
            }
            
            return MMHRecord.from_dict(record_dict)
    
    def search_records(self, 
                      tags: Optional[List[str]] = None,
                      domain: Optional[str] = None,
                      record_type: Optional[str] = None,
                      author: Optional[str] = None,
                      limit: Optional[int] = None) -> List[MMHRecord]:
        """Search MMH records with database queries"""
        query = "SELECT * FROM mmh_records WHERE 1=1"
        params = []
        
        if domain:
            query += " AND domain = ?"
            params.append(domain)
        
        if record_type:
            query += " AND record_type = ?"
            params.append(record_type)
        
        if author:
            query += " AND author = ?"
            params.append(author)
        
        query += " ORDER BY timestamp DESC"
        
        if limit:
            query += f" LIMIT {limit}"
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            
            records = []
            for row in cursor.fetchall():
                record_dict = {
                    "mmh_id": row[0],
                    "timestamp": row[1],
                    "record_type": row[2],
                    "domain": row[3],
                    "content_hash": row[4],
                    "content_data": json.loads(row[5]),
                    "content_size": row[6],
                    "signature": row[7],
                    "verification_hash": row[8],
                    "chain_hash": row[9],
                    "tags": json.loads(row[10]),
                    "description": row[11],
                    "author": row[12],
                    "version": row[13],
                    "test_name": row[14],
                    "reproducibility_score": row[15]
                }
                
                record = MMHRecord.from_dict(record_dict)
                
                # Apply tag filtering if specified
                if tags:
                    if not any(tag in record.tags for tag in tags):
                        continue
                
                records.append(record)
            
            return records
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get MMH database statistics"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Total records
            cursor.execute("SELECT COUNT(*) FROM mmh_records")
            total_records = cursor.fetchone()[0]
            
            # Records by type
            cursor.execute("""
                SELECT record_type, COUNT(*) 
                FROM mmh_records 
                GROUP BY record_type
            """)
            records_by_type = dict(cursor.fetchall())
            
            # Records by domain
            cursor.execute("""
                SELECT domain, COUNT(*) 
                FROM mmh_records 
                GROUP BY domain
            """)
            records_by_domain = dict(cursor.fetchall())
            
            # Total storage size
            cursor.execute("SELECT SUM(content_size) FROM mmh_records")
            total_size = cursor.fetchone()[0] or 0
            
            # Average reproducibility score
            cursor.execute("""
                SELECT AVG(reproducibility_score) 
                FROM mmh_records 
                WHERE reproducibility_score IS NOT NULL
            """)
            avg_reproducibility = cursor.fetchone()[0] or 0.0
            
            return {
                "total_records": total_records,
                "records_by_type": records_by_type,
                "records_by_domain": records_by_domain,
                "total_size_bytes": total_size,
                "total_size_mb": total_size / (1024 * 1024),
                "average_reproducibility_score": avg_reproducibility
            }


class MMHStorage:
    """
    Comprehensive MMH storage system with database and file backup
    """
    
    def __init__(self, storage_path: str = "mmh_storage"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(exist_ok=True)
        
        # Initialize components
        self.database = MMHDatabase(self.storage_path / "mmh.db")
        self.backup_path = self.storage_path / "backups"
        self.backup_path.mkdir(exist_ok=True)
    
    def store_record(self, record: MMHRecord):
        """Store MMH record in both database and file backup"""
        # Store in database
        self.database.store_record(record)
        
        # Create file backup
        self._create_file_backup(record)
    
    def _create_file_backup(self, record: MMHRecord):
        """Create compressed file backup of MMH record"""
        backup_file = self.backup_path / f"{record.mmh_id}.mmh"
        
        # Compress record data
        record_data = {
            "record": record.to_dict(),
            "backup_timestamp": datetime.utcnow().isoformat(),
            "backup_version": "1.0.0"
        }
        
        with gzip.open(backup_file, 'wt', encoding='utf-8') as f:
            json.dump(record_data, f, indent=2)
    
    def get_record(self, mmh_id: str) -> Optional[MMHRecord]:
        """Retrieve MMH record from database"""
        return self.database.get_record(mmh_id)
    
    def search_records(self, **kwargs) -> List[MMHRecord]:
        """Search MMH records"""
        return self.database.search_records(**kwargs)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get storage statistics"""
        db_stats = self.database.get_statistics()
        
        # Add file backup statistics
        backup_files = list(self.backup_path.glob("*.mmh"))
        db_stats["backup_files"] = len(backup_files)
        db_stats["backup_size_mb"] = sum(f.stat().st_size for f in backup_files) / (1024 * 1024)
        
        return db_stats
    
    def create_backup(self, backup_name: str = None) -> str:
        """Create complete backup of MMH storage"""
        if not backup_name:
            backup_name = f"mmh_backup_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        backup_dir = self.backup_path / backup_name
        backup_dir.mkdir(exist_ok=True)
        
        # Copy database
        shutil.copy2(self.database.db_path, backup_dir / "mmh.db")
        
        # Copy all backup files
        backup_files_dir = backup_dir / "backups"
        backup_files_dir.mkdir(exist_ok=True)
        
        for backup_file in self.backup_path.glob("*.mmh"):
            shutil.copy2(backup_file, backup_files_dir / backup_file.name)
        
        # Create backup manifest
        manifest = {
            "backup_name": backup_name,
            "backup_timestamp": datetime.utcnow().isoformat(),
            "database_path": str(self.database.db_path),
            "backup_files_count": len(list(self.backup_path.glob("*.mmh"))),
            "statistics": self.get_statistics()
        }
        
        with open(backup_dir / "manifest.json", 'w') as f:
            json.dump(manifest, f, indent=2)
        
        return str(backup_dir)
    
    def restore_from_backup(self, backup_path: str) -> bool:
        """Restore MMH storage from backup"""
        backup_dir = Path(backup_path)
        
        if not backup_dir.exists():
            return False
        
        # Restore database
        backup_db = backup_dir / "mmh.db"
        if backup_db.exists():
            shutil.copy2(backup_db, self.database.db_path)
        
        # Restore backup files
        backup_files_dir = backup_dir / "backups"
        if backup_files_dir.exists():
            for backup_file in backup_files_dir.glob("*.mmh"):
                shutil.copy2(backup_file, self.backup_path / backup_file.name)
        
        return True
    
    def verify_storage_integrity(self) -> Dict[str, Any]:
        """Verify integrity of stored MMH records"""
        integrity_report = {
            "database_records": 0,
            "backup_files": 0,
            "missing_backups": [],
            "corrupted_records": [],
            "integrity_verified": True
        }
        
        # Check database records
        with sqlite3.connect(self.database.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT mmh_id FROM mmh_records")
            db_records = {row[0] for row in cursor.fetchall()}
            integrity_report["database_records"] = len(db_records)
        
        # Check backup files
        backup_files = {f.stem for f in self.backup_path.glob("*.mmh")}
        integrity_report["backup_files"] = len(backup_files)
        
        # Find missing backups
        missing_backups = db_records - backup_files
        integrity_report["missing_backups"] = list(missing_backups)
        
        if missing_backups:
            integrity_report["integrity_verified"] = False
        
        # Check for corrupted records
        for mmh_id in db_records:
            record = self.get_record(mmh_id)
            if record and not self._verify_record_integrity(record):
                integrity_report["corrupted_records"].append(mmh_id)
                integrity_report["integrity_verified"] = False
        
        return integrity_report
    
    def _verify_record_integrity(self, record: MMHRecord) -> bool:
        """Verify individual record integrity"""
        try:
            # Basic integrity checks
            if not record.mmh_id or not record.content_hash:
                return False
            
            # Check content hash
            import gzip
            content_str = json.dumps(record.content_data, sort_keys=True)
            compressed_content = gzip.compress(content_str.encode())
            expected_hash = hashlib.sha256(compressed_content).hexdigest()
            
            return record.content_hash == expected_hash
            
        except Exception:
            return False 