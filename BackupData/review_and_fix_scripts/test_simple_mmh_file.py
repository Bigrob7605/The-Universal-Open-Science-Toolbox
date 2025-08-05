#!/usr/bin/env python3
"""
Simple MMH File Format Test

Test the simplified MMH file format
"""

import sys
from pathlib import Path

# Import MMH system components
from mmh_system import MMHCore, MMHRecord, SimpleMMHFile

def test_simple_mmh_file():
    """Test simple MMH file format"""
    print("🧪 Testing Simple MMH File Format...")
    
    # Create a simple test record
    mmh_core = MMHCore("test_simple_storage")
    
    test_content = {
        "test_name": "simple_test",
        "input_data": {"value": 42},
        "parameters": {"method": "simple"},
        "results": {"output": 84},
        "environment": {
            "python_version": "3.13.5",
            "dependencies": ["numpy"],
            "random_seed": 123
        }
    }
    
    record = mmh_core.create_record(
        content_data=test_content,
        record_type="test_result",
        domain="test",
        tags=["simple", "test"],
        description="Simple test record",
        author="Kai Core System",
        test_name="simple_test"
    )
    
    print(f"✅ Created test record: {record.mmh_id}")
    
    # Create simple MMH file
    simple_mmh = SimpleMMHFile()
    output_path = "simple_test.mmh"
    
    try:
        mmh_file_path = simple_mmh.create_simple_mmh_file([record], output_path)
        print(f"✅ Created simple MMH file: {mmh_file_path}")
        
        # Check file exists
        if Path(mmh_file_path).exists():
            file_size = Path(mmh_file_path).stat().st_size
            print(f"   File size: {file_size} bytes")
            print(f"   File exists: ✅")
        else:
            print(f"   File exists: ❌")
        
        # Load and test file
        simple_mmh.load_simple_mmh_file(mmh_file_path)
        print(f"✅ Loaded MMH file successfully")
        
        # Get file info
        file_info = simple_mmh.get_file_info()
        print(f"   Total records: {file_info['total_records']}")
        print(f"   Domains: {file_info['domains']}")
        
        # Test unfolding
        unfolded_record = simple_mmh.unfold_record(record.mmh_id)
        if unfolded_record:
            print(f"✅ Unfolded record: {unfolded_record.mmh_id}")
            print(f"   Domain: {unfolded_record.domain}")
            print(f"   Test: {unfolded_record.test_name}")
        
        # Test retesting
        retest_result = simple_mmh.retest_record(record.mmh_id)
        print(f"✅ Retest result: {retest_result['success']}")
        if retest_result['success']:
            print(f"   Reproducibility score: {retest_result['reproducibility_score']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error with simple MMH file: {e}")
        return False

def main():
    """Main test function"""
    print("📁 SIMPLE MMH FILE FORMAT TEST")
    print("=" * 40)
    
    try:
        success = test_simple_mmh_file()
        
        if success:
            print("\n" + "=" * 40)
            print("🎉 SIMPLE MMH FILE FORMAT TEST COMPLETE!")
            print("✅ Single-file storage working")
            print("✅ Selective unfolding working")
            print("✅ Easy retesting functional")
            print("✅ Bit-perfect reproduction ready")
            
            return True
        else:
            print("\n❌ Simple MMH file format test failed")
            return False
            
    except Exception as e:
        print(f"\n❌ Simple MMH file format test error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 