"""
Smoke tests for Universal Open Science Toolbox.
Basic tests to ensure the framework works correctly.
"""

import pytest
import numpy as np
import pandas as pd
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from BULLETPROOF_PIPELINE import BulletproofPipeline
from test_suite.universal_test_functions import (
    basic_statistical_analysis,
    correlation_analysis,
    signal_detection_test,
    periodicity_test,
    clustering_analysis,
    dimensionality_analysis,
    get_available_tests
)


def test_pipeline_import():
    """Test that the pipeline can be imported."""
    assert BulletproofPipeline is not None


def test_pipeline_initialization():
    """Test that the pipeline can be initialized."""
    pipeline = BulletproofPipeline()
    assert pipeline is not None
    assert hasattr(pipeline, 'load_data')
    assert hasattr(pipeline, 'run_test')


def test_basic_statistical_analysis():
    """Test basic statistical analysis function."""
    # Create test data
    data = np.random.normal(0, 1, (100, 3))
    
    # Run analysis
    result = basic_statistical_analysis(data)
    
    # Check that result has expected structure
    assert "metrics" in result
    assert "pass_fail" in result
    assert isinstance(result["pass_fail"], dict)
    
    # Check that metrics contains expected fields
    metrics = result["metrics"]
    assert "mean" in metrics
    assert "std" in metrics
    
    # Check that pass/fail contains boolean values
    for key, value in result["pass_fail"].items():
        assert isinstance(value, bool), f"Pass/fail value for {key} should be boolean"


def test_correlation_analysis():
    """Test correlation analysis function."""
    # Create test data with correlation
    np.random.seed(42)
    x = np.random.normal(0, 1, 100)
    y = x + np.random.normal(0, 0.1, 100)  # Correlated with x
    data = np.column_stack([x, y])
    
    # Run analysis
    result = correlation_analysis(data)
    
    # Check structure
    assert "metrics" in result
    assert "pass_fail" in result
    assert isinstance(result["pass_fail"], dict)
    
    # Check that metrics contains expected fields
    metrics = result["metrics"]
    assert "pearson_correlation" in metrics


def test_signal_detection():
    """Test signal detection function."""
    # Create test signal
    t = np.linspace(0, 10, 1000)
    signal = 3 * np.sin(2 * np.pi * 2 * t)  # 2 Hz signal
    noise = np.random.normal(0, 1, 1000)
    data = signal + noise
    
    # Run analysis
    result = signal_detection_test(data)
    
    # Check structure
    assert "metrics" in result
    assert "pass_fail" in result
    assert isinstance(result["pass_fail"], dict)
    
    # Check that metrics contains expected fields
    metrics = result["metrics"]
    assert "signal_statistics" in metrics


def test_periodicity_test():
    """Test periodicity detection function."""
    # Create periodic data
    t = np.linspace(0, 20, 200)
    data = np.sin(2 * np.pi * 0.1 * t) + np.random.normal(0, 0.1, 200)
    
    # Run analysis
    result = periodicity_test(data)
    
    # Check structure
    assert "metrics" in result
    assert "pass_fail" in result
    assert isinstance(result["pass_fail"], dict)
    
    # Check that metrics contains expected fields
    metrics = result["metrics"]
    assert "periodicity_summary" in metrics


def test_clustering_analysis():
    """Test clustering analysis function."""
    # Create clustered data
    np.random.seed(42)
    cluster1 = np.random.normal(0, 1, (50, 2))
    cluster2 = np.random.normal(5, 1, (50, 2))
    data = np.vstack([cluster1, cluster2])
    
    # Run analysis
    result = clustering_analysis(data, max_clusters=4)
    
    # Check structure
    assert "metrics" in result
    assert "pass_fail" in result
    assert isinstance(result["pass_fail"], dict)
    
    # Check that metrics contains expected fields
    metrics = result["metrics"]
    assert "cluster_analysis" in metrics
    assert "optimal_clusters" in metrics


def test_dimensionality_analysis():
    """Test dimensionality analysis function."""
    # Create test data
    data = np.random.normal(0, 1, (100, 5))
    
    # Run analysis
    result = dimensionality_analysis(data)
    
    # Check structure
    assert "metrics" in result
    assert "pass_fail" in result
    assert isinstance(result["pass_fail"], dict)
    
    # Check that metrics contains expected fields
    metrics = result["metrics"]
    assert "dimensions" in metrics
    assert "effective_dimensions" in metrics


def test_get_available_tests():
    """Test that available tests can be listed."""
    tests = get_available_tests()
    assert isinstance(tests, dict)
    assert len(tests) > 0
    
    # Check that all tests have descriptions
    for test_name, description in tests.items():
        assert isinstance(test_name, str)
        assert isinstance(description, str)
        assert len(description) > 0


def test_pipeline_data_loading():
    """Test that the pipeline can load data."""
    pipeline = BulletproofPipeline()
    
    # Create test data file
    test_data = np.random.normal(0, 1, (50, 3))
    test_file = "test_data_temp.csv"
    pd.DataFrame(test_data).to_csv(test_file, index=False)
    
    try:
        # Test data loading
        success = pipeline.load_data(test_file, "csv")
        assert success
        
        # Check that data was loaded
        assert hasattr(pipeline, 'data')
        assert pipeline.data is not None
        
    finally:
        # Clean up
        if os.path.exists(test_file):
            os.remove(test_file)


def test_pipeline_test_registration():
    """Test that custom tests can be registered."""
    pipeline = BulletproofPipeline()
    
    def custom_test(data, **kwargs):
        return {"custom_metric": 42.0, "pass_fail": {"test_passed": True}}
    
    # Register test
    pipeline.register_test_function("custom_test", custom_test)
    
    # Check that test was registered
    assert "custom_test" in pipeline.test_functions


def test_error_handling():
    """Test that the framework handles errors gracefully."""
    # Test with invalid data
    result = basic_statistical_analysis(None)
    assert "metrics" in result
    assert "pass_fail" in result
    
    # Test with empty data
    result = basic_statistical_analysis(np.array([]))
    assert "metrics" in result
    assert "pass_fail" in result


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"]) 