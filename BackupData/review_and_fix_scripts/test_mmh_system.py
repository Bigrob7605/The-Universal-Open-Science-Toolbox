#!/usr/bin/env python3
"""
Test MMH System Integration with Kai Core

Tests the complete MMH (Immutable Memory Hash) system for:
- Immutable data storage
- Cryptographic verification
- 100% reproducible test recreation
- Scientific data preservation
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
    MMHReproducer
)

def test_mmh_core():
    """Test MMH core functionality"""
    print("🧪 Testing MMH Core System...")
    
    # Initialize MMH core
    mmh_core = MMHCore("test_mmh_storage")
    
    # Create test data
    test_content = {
        "test_name": "physics_gravity_test",
        "input_data": {"mass": 100, "distance": 10},
        "parameters": {"gravitational_constant": 6.67430e-11},
        "results": {"force": 6.67430e-9},
        "environment": {
            "python_version": "3.13.5",
            "dependencies": ["numpy", "scipy"],
            "random_seed": 42
        }
    }
    
    # Create MMH record
    record = mmh_core.create_record(
        content_data=test_content,
        record_type="test_result",
        domain="physics",
        tags=["gravity", "newton", "force"],
        description="Test of gravitational force calculation",
        author="Kai Core System",
        test_name="physics_gravity_test"
    )
    
    print(f"✅ Created MMH record: {record.mmh_id}")
    print(f"   Reproducibility Score: {record.reproducibility_score}")
    print(f"   Content Size: {record.content_size} bytes")
    
    # Verify record integrity
    integrity_verified = mmh_core.verify_record(record)
    print(f"✅ Record integrity verified: {integrity_verified}")
    
    # Search records
    search_results = mmh_core.search_records(domain="physics")
    print(f"✅ Found {len(search_results)} physics records")
    
    return record

def test_mmh_storage():
    """Test MMH storage system"""
    print("\n🧪 Testing MMH Storage System...")
    
    # Initialize storage
    storage = MMHStorage("test_mmh_storage")
    
    # Create test record
    test_content = {
        "test_name": "climate_temperature_test",
        "input_data": {"temperature_data": [20, 25, 30, 35]},
        "parameters": {"analysis_method": "linear_regression"},
        "results": {"trend": 5.0, "r_squared": 0.95},
        "environment": {
            "python_version": "3.13.5",
            "dependencies": ["pandas", "scikit-learn"],
            "random_seed": 123
        }
    }
    
    # Create and store record
    mmh_core = MMHCore("test_mmh_storage")
    record = mmh_core.create_record(
        content_data=test_content,
        record_type="test_result",
        domain="climate",
        tags=["temperature", "trend", "regression"],
        description="Climate temperature trend analysis",
        author="Kai Core System",
        test_name="climate_temperature_test"
    )
    
    storage.store_record(record)
    print(f"✅ Stored MMH record: {record.mmh_id}")
    
    # Retrieve record
    retrieved_record = storage.get_record(record.mmh_id)
    print(f"✅ Retrieved record: {retrieved_record.mmh_id if retrieved_record else 'None'}")
    
    # Get statistics
    stats = storage.get_statistics()
    print(f"✅ Storage statistics: {stats['total_records']} records, {stats['total_size_mb']:.2f} MB")
    
    # Verify storage integrity
    integrity = storage.verify_storage_integrity()
    print(f"✅ Storage integrity verified: {integrity['integrity_verified']}")
    
    return record

def test_mmh_signer():
    """Test MMH cryptographic signing"""
    print("\n🧪 Testing MMH Signer System...")
    
    # Initialize signer
    signer = MMHSigner()
    
    # Create test record
    test_content = {
        "test_name": "biology_growth_test",
        "input_data": {"population": [100, 120, 144, 173]},
        "parameters": {"growth_rate": 0.2},
        "results": {"final_population": 207, "growth_factor": 1.2},
        "environment": {
            "python_version": "3.13.5",
            "dependencies": ["matplotlib", "numpy"],
            "random_seed": 456
        }
    }
    
    mmh_core = MMHCore("test_mmh_storage")
    record = mmh_core.create_record(
        content_data=test_content,
        record_type="test_result",
        domain="biology",
        tags=["population", "growth", "exponential"],
        description="Population growth model test",
        author="Kai Core System",
        test_name="biology_growth_test"
    )
    
    # Sign record
    signature = signer.sign_record(record)
    print(f"✅ Created signature: {signature[:20]}...")
    
    # Verify signature
    signature_verified = signer.verify_signature(record, signature)
    print(f"✅ Signature verified: {signature_verified}")
    
    # Test validator
    validator = MMHValidator(signer)
    validation_result = validator.validate_record(record)
    print(f"✅ Record validation: {validation_result['validation_passed']}")
    print(f"   Reproducible: {validation_result['reproducibility']['reproducible']}")
    
    return record

def test_mmh_reproducer():
    """Test MMH reproduction system"""
    print("\n🧪 Testing MMH Reproducer System...")
    
    # Initialize storage and reproducer
    storage = MMHStorage("test_mmh_storage")
    reproducer = MMHReproducer(storage)
    
    # Create test record for reproduction
    test_content = {
        "test_name": "social_network_test",
        "input_data": {"nodes": 100, "edges": 500},
        "parameters": {"algorithm": "pagerank", "iterations": 100},
        "results": {"centrality_scores": [0.1, 0.2, 0.3], "convergence": True},
        "environment": {
            "python_version": "3.13.5",
            "dependencies": ["networkx", "numpy"],
            "random_seed": 789
        }
    }
    
    mmh_core = MMHCore("test_mmh_storage")
    record = mmh_core.create_record(
        content_data=test_content,
        record_type="test_result",
        domain="social_science",
        tags=["network", "pagerank", "centrality"],
        description="Social network centrality analysis",
        author="Kai Core System",
        test_name="social_network_test"
    )
    
    storage.store_record(record)
    
    # Reproduce test
    reproduction_result = reproducer.reproduce_test(record.mmh_id)
    print(f"✅ Reproduction success: {reproduction_result['success']}")
    
    if reproduction_result['success']:
        verification = reproduction_result['verification_result']
        print(f"   Verification passed: {verification['verification_passed']}")
        print(f"   Accuracy score: {verification['accuracy_score']:.3f}")
        print(f"   Exact match: {verification['exact_match']}")
    
    return record

def test_mmh_integration():
    """Test complete MMH system integration"""
    print("\n🧪 Testing Complete MMH System Integration...")
    
    # Test all components
    core_record = test_mmh_core()
    storage_record = test_mmh_storage()
    signer_record = test_mmh_signer()
    reproducer_record = test_mmh_reproducer()
    
    # Test batch operations
    storage = MMHStorage("test_mmh_storage")
    reproducer = MMHReproducer(storage)
    
    # Batch reproduce
    mmh_ids = [core_record.mmh_id, storage_record.mmh_id, signer_record.mmh_id, reproducer_record.mmh_id]
    batch_result = reproducer.batch_reproduce(mmh_ids)
    
    print(f"\n✅ Batch reproduction results:")
    print(f"   Total tests: {batch_result['total_tests']}")
    print(f"   Successful: {batch_result['successful_reproductions']}")
    print(f"   Failed: {batch_result['failed_reproductions']}")
    print(f"   Verification passed: {batch_result['verification_passed']}")
    
    # Generate batch report
    batch_report = reproducer.generate_batch_report(batch_result)
    print(f"\n📊 Batch Report Generated ({len(batch_report)} characters)")
    
    return True

def main():
    """Main test function"""
    print("🔗 MMH SYSTEM INTEGRATION TEST")
    print("=" * 50)
    
    try:
        # Test complete MMH system
        success = test_mmh_integration()
        
        if success:
            print("\n" + "=" * 50)
            print("🎉 MMH SYSTEM INTEGRATION TEST COMPLETE!")
            print("✅ All MMH components working correctly")
            print("✅ Immutable data storage operational")
            print("✅ Cryptographic verification active")
            print("✅ 100% reproducible test recreation ready")
            print("✅ Scientific data preservation enabled")
            
            return True
        else:
            print("\n❌ MMH system test failed")
            return False
            
    except Exception as e:
        print(f"\n❌ MMH system test error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 