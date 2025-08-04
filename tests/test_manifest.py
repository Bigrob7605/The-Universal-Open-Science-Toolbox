"""
Manifest & Logging Tests
=======================

Tests for manifest creation and logging functionality.
"""

import pytest
import os
import json
import sys
import tempfile
import hashlib
import numpy as np
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from BULLETPROOF_PIPELINE import BulletproofPipeline


def test_manifest_creation():
    """Test that manifests are created correctly."""
    # Create test file
    test_data = "test content for manifest"
    test_file = "testfile.csv"
    
    with open(test_file, 'w') as f:
        f.write(test_data)
    
    try:
        # Calculate hash
        with open(test_file, 'rb') as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()
        
        # Create manifest directory if it doesn't exist
        manifest_dir = Path("manifests")
        manifest_dir.mkdir(exist_ok=True)
        
        # Create manifest
        manifest = {
            "file_name": test_file,
            "hash_algorithm": "sha256",
            "file_hash": file_hash,
            "dataset_name": "iris",
            "timestamp": "2024-01-01T00:00:00",
            "file_size": len(test_data),
            "data_type": "csv"
        }
        
        manifest_file = manifest_dir / f"{test_file}.manifest.json"
        with open(manifest_file, 'w') as f:
            json.dump(manifest, f, indent=2)
        
        # Test that manifest was created
        assert manifest_file.exists()
        
        # Test manifest content
        with open(manifest_file, 'r') as f:
            loaded_manifest = json.load(f)
        
        assert loaded_manifest["file_name"] == test_file
        assert loaded_manifest["hash_algorithm"] == "sha256"
        assert loaded_manifest["file_hash"] == file_hash
        assert loaded_manifest["dataset_name"] == "iris"
        
    finally:
        # Clean up
        if os.path.exists(test_file):
            os.remove(test_file)
        if manifest_file.exists():
            manifest_file.unlink()


def test_pipeline_manifest_generation():
    """Test that pipeline generates manifests correctly."""
    pipeline = BulletproofPipeline()
    
    # Create test data file
    test_data = np.random.normal(0, 1, (10, 3))
    test_file = "temp_manifest_test.csv"
    np.savetxt(test_file, test_data, delimiter=',', header='col1,col2,col3')
    
    try:
        # Load data (should generate manifest)
        success = pipeline.load_data(test_file, "csv")
        assert success
        
        # Check that manifest was created
        assert hasattr(pipeline, 'data_manifest')
        assert pipeline.data_manifest is not None
        assert 'shape' in pipeline.data_manifest
        assert 'data_type' in pipeline.data_manifest
        assert 'hash' in pipeline.data_manifest
    finally:
        if os.path.exists(test_file):
            os.remove(test_file)


def test_pipeline_logging():
    """Test that pipeline logs events correctly."""
    pipeline = BulletproofPipeline()
    
    # Check that logging is initialized
    assert hasattr(pipeline, 'log_entries')
    assert isinstance(pipeline.log_entries, list)
    
    # Check that startup log exists
    assert len(pipeline.log_entries) > 0
    startup_logs = [entry for entry in pipeline.log_entries if "PIPELINE_START" in entry["event_type"]]
    assert len(startup_logs) > 0
    
    # Check log entry structure
    for entry in pipeline.log_entries:
        assert "timestamp" in entry
        assert "event_type" in entry
        assert "data" in entry


def test_pipeline_log_event():
    """Test that pipeline can log custom events."""
    pipeline = BulletproofPipeline()
    initial_log_count = len(pipeline.log_entries)
    
    # Log a custom event
    pipeline._log_event("TEST_EVENT", {"test_data": "test_value"})
    
    # Check that log was added
    assert len(pipeline.log_entries) == initial_log_count + 1
    
    # Check the new log entry
    new_entry = pipeline.log_entries[-1]
    assert new_entry["event_type"] == "TEST_EVENT"
    assert new_entry["data"]["test_data"] == "test_value"


def test_pipeline_data_manifest_structure():
    """Test that data manifest has correct structure."""
    pipeline = BulletproofPipeline()
    
    # Create test data file
    test_data = np.random.normal(0, 1, (10, 3))
    test_file = "temp_manifest_structure.csv"
    np.savetxt(test_file, test_data, delimiter=',', header='col1,col2,col3')
    
    try:
        # Load test data
        success = pipeline.load_data(test_file, "csv")
        assert success
        
        # Check manifest structure
        manifest = pipeline.data_manifest
        required_keys = ['source_path', 'data_type', 'shape', 'hash', 'load_time']
        
        for key in required_keys:
            assert key in manifest, f"Manifest missing key: {key}"
    finally:
        if os.path.exists(test_file):
            os.remove(test_file)


def test_pipeline_save_results_with_manifest():
    """Test that pipeline saves results with manifest information."""
    pipeline = BulletproofPipeline()
    
    # Create test data file
    test_data = np.random.normal(0, 1, (10, 3))
    test_file = "temp_save_test.csv"
    np.savetxt(test_file, test_data, delimiter=',', header='col1,col2,col3')
    
    try:
        # Register test function
        from test_suite.universal_test_functions import basic_statistical_analysis
        pipeline.register_test_function("basic_statistical_analysis", basic_statistical_analysis)
        
        # Load data and run test
        pipeline.load_data(test_file, "csv")
        report = pipeline.run_batch_tests(["basic_statistical_analysis"])
        
        # Save results
        output_path = pipeline.save_results()
        assert output_path is not None
        assert os.path.exists(output_path)
        
        # Check that results file contains manifest info
        with open(output_path, 'r') as f:
            results = json.load(f)
        
        assert "data_manifest" in results
        assert results["data_manifest"] is not None
    finally:
        if os.path.exists(test_file):
            os.remove(test_file)


def test_pipeline_generate_report_with_manifest():
    """Test that pipeline generates reports with manifest information."""
    pipeline = BulletproofPipeline()
    
    # Create test data file
    test_data = np.random.normal(0, 1, (10, 3))
    test_file = "temp_report_test.csv"
    np.savetxt(test_file, test_data, delimiter=',', header='col1,col2,col3')
    
    try:
        # Register test function
        from test_suite.universal_test_functions import basic_statistical_analysis
        pipeline.register_test_function("basic_statistical_analysis", basic_statistical_analysis)
        
        # Load data and run test
        pipeline.load_data(test_file, "csv")
        report = pipeline.run_batch_tests(["basic_statistical_analysis"])
        
        # Generate report
        report_path = pipeline.generate_report()
        assert report_path is not None
        assert os.path.exists(report_path)
        
        # Check that report contains manifest info
        with open(report_path, 'r') as f:
            report_content = f.read()
        
        assert "Data Manifest" in report_content
    finally:
        if os.path.exists(test_file):
            os.remove(test_file)


def test_manifest_validation():
    """Test that manifests can be validated."""
    # Create test manifest
    test_manifest = {
        "file_name": "test.csv",
        "hash_algorithm": "sha256",
        "file_hash": "abc123",
        "dataset_name": "test_dataset",
        "timestamp": "2024-01-01T00:00:00",
        "file_size": 100,
        "data_type": "csv"
    }
    
    # Test required fields
    required_fields = ["file_name", "hash_algorithm", "file_hash", "dataset_name"]
    for field in required_fields:
        assert field in test_manifest, f"Manifest missing required field: {field}"
    
    # Test data types
    assert isinstance(test_manifest["file_name"], str)
    assert isinstance(test_manifest["hash_algorithm"], str)
    assert isinstance(test_manifest["file_hash"], str)
    assert isinstance(test_manifest["dataset_name"], str)


def test_manifest_file_integrity():
    """Test that manifest files maintain integrity."""
    # Create test file
    test_content = "test data for integrity check"
    test_file = "integrity_test.csv"
    
    with open(test_file, 'w') as f:
        f.write(test_content)
    
    try:
        # Calculate hash
        with open(test_file, 'rb') as f:
            original_hash = hashlib.sha256(f.read()).hexdigest()
        
        # Create manifest
        manifest = {
            "file_name": test_file,
            "hash_algorithm": "sha256",
            "file_hash": original_hash,
            "dataset_name": "integrity_test",
            "timestamp": "2024-01-01T00:00:00"
        }
        
        # Save manifest
        manifest_file = f"{test_file}.manifest.json"
        with open(manifest_file, 'w') as f:
            json.dump(manifest, f, indent=2)
        
        # Verify manifest can be loaded
        with open(manifest_file, 'r') as f:
            loaded_manifest = json.load(f)
        
        assert loaded_manifest["file_hash"] == original_hash
        
        # Verify file hasn't changed
        with open(test_file, 'rb') as f:
            current_hash = hashlib.sha256(f.read()).hexdigest()
        
        assert current_hash == original_hash
        
    finally:
        # Clean up
        if os.path.exists(test_file):
            os.remove(test_file)
        if os.path.exists(manifest_file):
            os.remove(manifest_file)


def test_pipeline_logging_timestamp():
    """Test that pipeline logs have proper timestamps."""
    pipeline = BulletproofPipeline()
    
    # Check that all log entries have timestamps
    for entry in pipeline.log_entries:
        assert "timestamp" in entry
        timestamp = entry["timestamp"]
        
        # Check timestamp format (ISO format)
        assert "T" in timestamp  # Should contain T separator
        assert len(timestamp) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 