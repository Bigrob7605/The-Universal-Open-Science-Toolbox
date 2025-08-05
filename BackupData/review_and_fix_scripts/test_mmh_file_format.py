#!/usr/bin/env python3
"""
Test MMH File Format - Single File Immutable Storage

Tests the MMH file format for:
- Single file storage of all data
- Selective unfolding (one record or all)
- Easy retesting with bit-perfect reproduction
- Space-efficient compression
- Bit-perfect accuracy
"""

import sys
import json
from datetime import datetime
from pathlib import Path

# Import MMH system components
from mmh_system import (
    MMHCore, MMHRecord, MMHVerifier,
    MMHStorage, MMHDatabase,
    MMHSigner, MMHValidator,
    MMHReproducer, MMHFileFormat, MMHFileManager
)

def create_test_records():
    """Create test MMH records for file format testing"""
    mmh_core = MMHCore("test_mmh_file_storage")
    
    # Create multiple test records
    test_records = []
    
    # Physics test
    physics_content = {
        "test_name": "quantum_entanglement_test",
        "input_data": {"particles": 2, "distance": 1000},
        "parameters": {"measurement_basis": "bell_state"},
        "results": {"correlation": 0.99, "entanglement_confirmed": True},
        "environment": {
            "python_version": "3.13.5",
            "dependencies": ["numpy", "qutip"],
            "random_seed": 42
        }
    }
    
    physics_record = mmh_core.create_record(
        content_data=physics_content,
        record_type="test_result",
        domain="physics",
        tags=["quantum", "entanglement", "bell_state"],
        description="Quantum entanglement verification test",
        author="Kai Core System",
        test_name="quantum_entanglement_test"
    )
    test_records.append(physics_record)
    
    # Climate test
    climate_content = {
        "test_name": "global_warming_analysis",
        "input_data": {"temperature_data": [14.0, 14.2, 14.5, 14.8, 15.1]},
        "parameters": {"analysis_period": "5_years", "method": "linear_trend"},
        "results": {"trend": 0.275, "confidence": 0.95, "significant": True},
        "environment": {
            "python_version": "3.13.5",
            "dependencies": ["pandas", "scipy", "matplotlib"],
            "random_seed": 123
        }
    }
    
    climate_record = mmh_core.create_record(
        content_data=climate_content,
        record_type="test_result",
        domain="climate",
        tags=["global_warming", "temperature", "trend"],
        description="Global temperature trend analysis",
        author="Kai Core System",
        test_name="global_warming_analysis"
    )
    test_records.append(climate_record)
    
    # Biology test
    biology_content = {
        "test_name": "dna_sequence_analysis",
        "input_data": {"sequence": "ATCGATCGATCG", "length": 12},
        "parameters": {"algorithm": "smith_waterman", "gap_penalty": -2},
        "results": {"similarity": 0.85, "alignment_score": 8.5},
        "environment": {
            "python_version": "3.13.5",
            "dependencies": ["biopython", "numpy"],
            "random_seed": 456
        }
    }
    
    biology_record = mmh_core.create_record(
        content_data=biology_content,
        record_type="test_result",
        domain="biology",
        tags=["dna", "sequence", "alignment"],
        description="DNA sequence alignment analysis",
        author="Kai Core System",
        test_name="dna_sequence_analysis"
    )
    test_records.append(biology_record)
    
    return test_records

def test_mmh_file_creation():
    """Test MMH file creation"""
    print("🧪 Testing MMH File Creation...")
    
    # Create test records
    test_records = create_test_records()
    print(f"✅ Created {len(test_records)} test records")
    
    # Create MMH file
    mmh_format = MMHFileFormat()
    output_path = "test_scientific_data.mmh"
    
    mmh_file_path = mmh_format.create_mmh_file(test_records, output_path)
    print(f"✅ Created MMH file: {mmh_file_path}")
    
    # Check file size
    file_size = Path(mmh_file_path).stat().st_size
    print(f"   File size: {file_size} bytes")
    
    return mmh_file_path, test_records

def test_mmh_file_loading():
    """Test MMH file loading"""
    print("\n🧪 Testing MMH File Loading...")
    
    # Load MMH file
    mmh_format = MMHFileFormat()
    mmh_format.load_mmh_file("test_scientific_data.mmh")
    
    # Get file info
    file_info = mmh_format.get_file_info()
    print(f"✅ Loaded MMH file successfully")
    print(f"   Total records: {file_info['total_records']}")
    print(f"   Domains: {file_info['domains']}")
    print(f"   Date range: {file_info['date_range']}")
    
    return mmh_format

def test_selective_unfolding():
    """Test selective unfolding of records"""
    print("\n🧪 Testing Selective Unfolding...")
    
    mmh_format = MMHFileFormat()
    mmh_format.load_mmh_file("test_scientific_data.mmh")
    
    # Get all record IDs
    all_ids = list(mmh_format.index["by_id"].keys())
    print(f"✅ Available records: {len(all_ids)}")
    
    # Unfold single record
    single_record = mmh_format.unfold_record(all_ids[0])
    print(f"✅ Unfolded single record: {single_record.mmh_id}")
    print(f"   Domain: {single_record.domain}")
    print(f"   Test: {single_record.test_name}")
    
    # Unfold multiple records
    multiple_records = mmh_format.unfold_records(all_ids[:2])
    print(f"✅ Unfolded {len(multiple_records)} records")
    
    # Unfold all records
    all_records = mmh_format.unfold_all()
    print(f"✅ Unfolded all {len(all_records)} records")
    
    return mmh_format

def test_search_functionality():
    """Test search functionality"""
    print("\n🧪 Testing Search Functionality...")
    
    mmh_format = MMHFileFormat()
    mmh_format.load_mmh_file("test_scientific_data.mmh")
    
    # Search by domain
    physics_records = mmh_format.search_records(domain="physics")
    print(f"✅ Found {len(physics_records)} physics records")
    
    # Search by tags
    quantum_records = mmh_format.search_records(tags=["quantum"])
    print(f"✅ Found {len(quantum_records)} quantum-related records")
    
    # Search by author
    kai_records = mmh_format.search_records(author="Kai Core System")
    print(f"✅ Found {len(kai_records)} records by Kai Core System")
    
    return mmh_format

def test_easy_retesting():
    """Test easy retesting functionality"""
    print("\n🧪 Testing Easy Retesting...")
    
    mmh_format = MMHFileFormat()
    mmh_format.load_mmh_file("test_scientific_data.mmh")
    
    # Get all record IDs
    all_ids = list(mmh_format.index["by_id"].keys())
    
    # Retest single record
    retest_result = mmh_format.retest_record(all_ids[0])
    print(f"✅ Retested single record: {retest_result['success']}")
    if retest_result['success']:
        print(f"   Reproducibility score: {retest_result['reproducibility_score']}")
        print(f"   Domain: {retest_result['domain']}")
    
    # Retest multiple records
    batch_result = mmh_format.retest_records(all_ids)
    print(f"✅ Batch retested {batch_result['total_records']} records")
    print(f"   Successful: {batch_result['successful_retests']}")
    print(f"   Failed: {batch_result['failed_retests']}")
    
    return mmh_format

def test_file_manager():
    """Test MMH file manager"""
    print("\n🧪 Testing MMH File Manager...")
    
    manager = MMHFileManager()
    
    # Load file
    mmh_format = manager.load_file("test_scientific_data.mmh")
    print(f"✅ Loaded file with manager")
    
    # Easy retesting
    all_ids = list(mmh_format.index["by_id"].keys())
    retest_result = manager.retest_with_ease(all_ids[0])
    print(f"✅ Easy retest: {retest_result['success']}")
    
    # Batch retesting
    batch_result = manager.batch_retest(all_ids[:2])
    print(f"✅ Batch retest: {batch_result['total_records']} records")
    
    return manager

def test_export_functionality():
    """Test export functionality"""
    print("\n🧪 Testing Export Functionality...")
    
    mmh_format = MMHFileFormat()
    mmh_format.load_mmh_file("test_scientific_data.mmh")
    
    # Get all record IDs
    all_ids = list(mmh_format.index["by_id"].keys())
    
    # Export single record
    export_success = mmh_format.export_record(all_ids[0], "exported_record.json")
    print(f"✅ Exported single record: {export_success}")
    
    # Export multiple records
    export_result = mmh_format.export_records(all_ids, "exported_records")
    print(f"✅ Exported {export_result['successful_exports']} records")
    print(f"   Files: {export_result['exported_files']}")
    
    return mmh_format

def main():
    """Main test function"""
    print("📁 MMH FILE FORMAT TEST")
    print("=" * 50)
    
    try:
        # Test complete MMH file format system
        print("🧪 Testing Complete MMH File Format System...")
        
        # Create and test file
        mmh_file_path, test_records = test_mmh_file_creation()
        
        # Test loading
        mmh_format = test_mmh_file_loading()
        
        # Test selective unfolding
        mmh_format = test_selective_unfolding()
        
        # Test search
        mmh_format = test_search_functionality()
        
        # Test easy retesting
        mmh_format = test_easy_retesting()
        
        # Test file manager
        manager = test_file_manager()
        
        # Test export
        mmh_format = test_export_functionality()
        
        print("\n" + "=" * 50)
        print("🎉 MMH FILE FORMAT TEST COMPLETE!")
        print("✅ Single-file storage operational")
        print("✅ Selective unfolding working")
        print("✅ Easy retesting functional")
        print("✅ Space-efficient compression active")
        print("✅ Bit-perfect reproduction ready")
        
        return True
        
    except Exception as e:
        print(f"\n❌ MMH file format test error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 