"""
Universal Test Function Coverage Tests
====================================

Tests to ensure all core tests output pass/fail and valid truth tables.
"""

import pytest
import numpy as np
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from test_suite.universal_test_functions import (
    basic_statistical_analysis,
    correlation_analysis,
    signal_detection_test,
    periodicity_test,
    clustering_analysis,
    dimensionality_analysis,
    get_available_tests
)


def test_basic_stats_pass_fail():
    """Test that basic statistical analysis returns pass/fail."""
    arr = np.random.normal(0, 1, (100, 5))
    result = basic_statistical_analysis(arr)
    assert "pass_fail" in result
    assert isinstance(result["pass_fail"], dict)
    
    # Check that all pass/fail values are booleans
    for key, value in result["pass_fail"].items():
        assert isinstance(value, bool), f"Pass/fail value for {key} should be boolean"


def test_correlation_analysis_pass_fail():
    """Test that correlation analysis returns pass/fail."""
    # Create correlated data
    np.random.seed(42)
    x = np.random.normal(0, 1, 100)
    y = x + np.random.normal(0, 0.1, 100)  # Correlated with x
    data = np.column_stack([x, y])
    
    result = correlation_analysis(data)
    assert "pass_fail" in result
    assert isinstance(result["pass_fail"], dict)
    
    # Check that all pass/fail values are booleans
    for key, value in result["pass_fail"].items():
        assert isinstance(value, bool), f"Pass/fail value for {key} should be boolean"


def test_signal_detection_pass_fail():
    """Test that signal detection returns pass/fail."""
    # Create test signal
    t = np.linspace(0, 10, 1000)
    signal = 3 * np.sin(2 * np.pi * 2 * t)  # 2 Hz signal
    noise = np.random.normal(0, 1, 1000)
    data = signal + noise
    
    result = signal_detection_test(data)
    assert "pass_fail" in result
    assert isinstance(result["pass_fail"], dict)
    
    # Check that all pass/fail values are booleans
    for key, value in result["pass_fail"].items():
        assert isinstance(value, bool), f"Pass/fail value for {key} should be boolean"


def test_periodicity_test_pass_fail():
    """Test that periodicity test returns pass/fail."""
    # Create periodic data
    t = np.linspace(0, 20, 200)
    data = np.sin(2 * np.pi * 0.1 * t) + np.random.normal(0, 0.1, 200)
    
    result = periodicity_test(data)
    assert "pass_fail" in result
    assert isinstance(result["pass_fail"], dict)
    
    # Check that all pass/fail values are booleans
    for key, value in result["pass_fail"].items():
        assert isinstance(value, bool), f"Pass/fail value for {key} should be boolean"


def test_clustering_analysis_pass_fail():
    """Test that clustering analysis returns pass/fail."""
    # Create clustered data
    np.random.seed(42)
    cluster1 = np.random.normal(0, 1, (50, 2))
    cluster2 = np.random.normal(5, 1, (50, 2))
    data = np.vstack([cluster1, cluster2])
    
    result = clustering_analysis(data, max_clusters=4)
    assert "pass_fail" in result
    assert isinstance(result["pass_fail"], dict)
    
    # Check that all pass/fail values are booleans
    for key, value in result["pass_fail"].items():
        assert isinstance(value, bool), f"Pass/fail value for {key} should be boolean"


def test_dimensionality_analysis_pass_fail():
    """Test that dimensionality analysis returns pass/fail."""
    data = np.random.normal(0, 1, (100, 5))
    
    result = dimensionality_analysis(data)
    assert "pass_fail" in result
    assert isinstance(result["pass_fail"], dict)
    
    # Check that all pass/fail values are booleans
    for key, value in result["pass_fail"].items():
        assert isinstance(value, bool), f"Pass/fail value for {key} should be boolean"


def test_truth_table_schema():
    """Test that all tests return valid truth table schema."""
    data = np.random.normal(0, 1, (50, 3))
    
    tests = [
        basic_statistical_analysis,
        correlation_analysis,
        signal_detection_test,
        periodicity_test,
        clustering_analysis,
        dimensionality_analysis
    ]
    
    for test_func in tests:
        result = test_func(data)
        
        # Check for either truth_table or pass_fail
        assert "truth_table" in result or "pass_fail" in result
        
        # If truth_table exists, check schema
        if "truth_table" in result:
            truth_table = result["truth_table"]
            assert isinstance(truth_table, list)
            if len(truth_table) > 0:
                assert "test_name" in truth_table[0]
                assert "timestamp" in truth_table[0]
                assert "pass_fail" in truth_table[0]


def test_all_tests_have_metrics():
    """Test that all tests return metrics."""
    data = np.random.normal(0, 1, (50, 3))
    
    tests = [
        basic_statistical_analysis,
        correlation_analysis,
        signal_detection_test,
        periodicity_test,
        clustering_analysis,
        dimensionality_analysis
    ]
    
    for test_func in tests:
        result = test_func(data)
        
        # Check for metrics or evidence
        assert "metrics" in result or "evidence" in result or any(
            key in result for key in ["mean", "std", "correlation", "signal_statistics", 
                                    "periodicity_summary", "cluster_analysis", "dimensions"]
        )


def test_all_tests_handle_errors():
    """Test that all tests handle errors gracefully."""
    tests = [
        basic_statistical_analysis,
        correlation_analysis,
        signal_detection_test,
        periodicity_test,
        clustering_analysis,
        dimensionality_analysis
    ]
    
    for test_func in tests:
        # Test with None
        result = test_func(None)
        assert "pass_fail" in result or "error" in result
        
        # Test with empty array
        result = test_func(np.array([]))
        assert "pass_fail" in result or "error" in result
        
        # Test with invalid data
        result = test_func("invalid_data")
        assert "pass_fail" in result or "error" in result


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


def test_test_reproducibility():
    """Test that tests are reproducible with same seed."""
    np.random.seed(42)
    data1 = np.random.normal(0, 1, (100, 3))
    
    np.random.seed(42)
    data2 = np.random.normal(0, 1, (100, 3))
    
    # Both datasets should be identical
    assert np.allclose(data1, data2)
    
    # Results should be identical
    result1 = basic_statistical_analysis(data1)
    result2 = basic_statistical_analysis(data2)
    
    # Check that pass/fail results are identical
    assert result1["pass_fail"] == result2["pass_fail"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 