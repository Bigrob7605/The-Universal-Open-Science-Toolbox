"""
Data Loader Tests for Universal Open Science Toolbox
==================================================

Tests for loading data in various formats (CSV, HDF5, FITS, NumPy).
"""

import pytest
import numpy as np
import pandas as pd
import os
import sys
import tempfile
import h5py

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from BULLETPROOF_PIPELINE import BulletproofPipeline


def test_load_csv():
    """Test loading CSV data."""
    # Create test CSV file
    test_data = np.random.normal(0, 1, (50, 3))
    test_file = "test_data.csv"
    pd.DataFrame(test_data, columns=['col1', 'col2', 'col3']).to_csv(test_file, index=False)
    
    try:
        pipeline = BulletproofPipeline()
        success = pipeline.load_data(test_file, "csv")
        assert success
        assert hasattr(pipeline, 'data')
        assert pipeline.data is not None
        assert pipeline.data.shape[0] > 0
    finally:
        if os.path.exists(test_file):
            os.remove(test_file)


def test_load_numpy():
    """Test loading NumPy data."""
    # Create test NumPy file
    test_data = np.random.normal(0, 1, (10, 3))
    test_file = "test_data.npy"
    np.save(test_file, test_data)
    
    try:
        pipeline = BulletproofPipeline()
        success = pipeline.load_data(test_file, "numpy")
        assert success
        assert hasattr(pipeline, 'data')
        assert pipeline.data is not None
        assert np.allclose(test_data, pipeline.data)
    finally:
        if os.path.exists(test_file):
            os.remove(test_file)


def test_load_hdf5():
    """Test loading HDF5 data."""
    # Create test HDF5 file
    test_data = np.random.normal(0, 1, (20, 4))
    test_file = "test_data.h5"
    
    with h5py.File(test_file, 'w') as f:
        f.create_dataset('data', data=test_data)
    
    try:
        pipeline = BulletproofPipeline()
        success = pipeline.load_data(test_file, "hdf5")
        assert success
        assert hasattr(pipeline, 'data')
        assert pipeline.data is not None
        assert pipeline.data.shape[0] > 0
    finally:
        if os.path.exists(test_file):
            os.remove(test_file)


def test_load_auto_detect():
    """Test automatic data type detection."""
    # Test CSV auto-detection
    test_data = np.random.normal(0, 1, (15, 2))
    test_file = "test_auto.csv"
    pd.DataFrame(test_data, columns=['x', 'y']).to_csv(test_file, index=False)
    
    try:
        pipeline = BulletproofPipeline()
        success = pipeline.load_data(test_file, "auto")
        assert success
        assert hasattr(pipeline, 'data')
        assert pipeline.data is not None
    finally:
        if os.path.exists(test_file):
            os.remove(test_file)


def test_load_existing_test_files():
    """Test loading existing test files in the project."""
    pipeline = BulletproofPipeline()
    
    # Test loading iris data
    if os.path.exists("test_data_iris.csv"):
        success = pipeline.load_data("test_data_iris.csv", "csv")
        assert success
        assert hasattr(pipeline, 'data')
        assert pipeline.data is not None
        assert pipeline.data.shape[0] > 0
    
    # Test loading wine data
    if os.path.exists("test_data_wine.csv"):
        success = pipeline.load_data("test_data_wine.csv", "csv")
        assert success
        assert hasattr(pipeline, 'data')
        assert pipeline.data is not None
        assert pipeline.data.shape[0] > 0


def test_load_data_validation():
    """Test data validation during loading."""
    pipeline = BulletproofPipeline()
    
    # Test with valid data file
    valid_data = np.random.normal(0, 1, (10, 3))
    test_file = "temp_valid_data.csv"
    np.savetxt(test_file, valid_data, delimiter=',', header='col1,col2,col3')
    
    try:
        success = pipeline.load_data(test_file, "csv")
        assert success
    finally:
        if os.path.exists(test_file):
            os.remove(test_file)
    
    # Test with non-existent file (should handle gracefully)
    success = pipeline.load_data("non_existent_file.csv", "csv")
    # Should handle gracefully, either succeed or fail gracefully
    assert isinstance(success, bool)


def test_load_data_manifest():
    """Test that data loading creates manifest."""
    test_data = np.random.normal(0, 1, (10, 3))
    test_file = "temp_manifest_data.csv"
    np.savetxt(test_file, test_data, delimiter=',', header='col1,col2,col3')
    
    pipeline = BulletproofPipeline()
    success = pipeline.load_data(test_file, "csv")
    
    assert success
    assert hasattr(pipeline, 'data_manifest')
    assert pipeline.data_manifest is not None
    assert 'shape' in pipeline.data_manifest
    assert 'data_type' in pipeline.data_manifest
    
    # Clean up
    if os.path.exists(test_file):
        os.remove(test_file)


def test_load_data_error_handling():
    """Test error handling for invalid data sources."""
    pipeline = BulletproofPipeline()
    
    # Test with non-existent file
    success = pipeline.load_data("non_existent_file.csv", "csv")
    # Should handle gracefully
    assert isinstance(success, bool)
    
    # Test with invalid data type
    success = pipeline.load_data("test_data_iris.csv", "invalid_type")
    # Should handle gracefully
    assert isinstance(success, bool)


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 