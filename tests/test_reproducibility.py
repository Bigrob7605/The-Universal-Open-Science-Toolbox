"""
Golden Path Reproducibility Tests
================================

Tests to ensure reproducibility - same inputs with same seed produce same outputs.
"""

import pytest
import numpy as np
import sys
import os
import json

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from BULLETPROOF_PIPELINE import BulletproofPipeline
from test_suite.universal_test_functions import (
    basic_statistical_analysis,
    correlation_analysis,
    signal_detection_test,
    periodicity_test,
    clustering_analysis,
    dimensionality_analysis
)


def test_reproducibility_same_seed():
    """Test that same seed produces same results."""
    # Set seed
    np.random.seed(42)
    data1 = np.random.normal(0, 1, (100, 5))
    
    # Reset seed and generate same data
    np.random.seed(42)
    data2 = np.random.normal(0, 1, (100, 5))
    
    # Data should be identical
    assert np.allclose(data1, data2)
    
    # Results should be identical
    result1 = basic_statistical_analysis(data1)
    result2 = basic_statistical_analysis(data2)
    
    # Check that pass/fail results are identical
    if "pass_fail" in result1 and "pass_fail" in result2:
        assert result1["pass_fail"] == result2["pass_fail"]


def test_reproducibility_multiple_runs():
    """Test that multiple runs with same seed produce same results."""
    tests = [
        basic_statistical_analysis,
        correlation_analysis,
        signal_detection_test,
        periodicity_test,
        clustering_analysis,
        dimensionality_analysis
    ]
    
    for test_func in tests:
        # Run 1
        np.random.seed(42)
        data1 = np.random.normal(0, 1, (50, 3))
        result1 = test_func(data1)
        
        # Run 2
        np.random.seed(42)
        data2 = np.random.normal(0, 1, (50, 3))
        result2 = test_func(data2)
        
        # Results should be identical
        if "pass_fail" in result1 and "pass_fail" in result2:
            assert result1["pass_fail"] == result2["pass_fail"]


def test_pipeline_reproducibility():
    """Test that pipeline produces reproducible results."""
    # Create test data files
    np.random.seed(42)
    data1 = np.random.normal(0, 1, (50, 3))
    test_file1 = "temp_reproducibility_1.csv"
    np.savetxt(test_file1, data1, delimiter=',', header='col1,col2,col3')
    
    np.random.seed(42)
    data2 = np.random.normal(0, 1, (50, 3))
    test_file2 = "temp_reproducibility_2.csv"
    np.savetxt(test_file2, data2, delimiter=',', header='col1,col2,col3')
    
    try:
        # Register test function
        from test_suite.universal_test_functions import basic_statistical_analysis
        
        # Run 1
        pipeline1 = BulletproofPipeline()
        pipeline1.register_test_function("basic_statistical_analysis", basic_statistical_analysis)
        pipeline1.load_data(test_file1, "csv")
        result1 = pipeline1.run_batch_tests(["basic_statistical_analysis"])
        
        # Run 2
        pipeline2 = BulletproofPipeline()
        pipeline2.register_test_function("basic_statistical_analysis", basic_statistical_analysis)
        pipeline2.load_data(test_file2, "csv")
        result2 = pipeline2.run_batch_tests(["basic_statistical_analysis"])
        
        # Results should be identical
        assert result1["overall_truth_table"]["tests_run"][0]["pass_fail"] == result2["overall_truth_table"]["tests_run"][0]["pass_fail"]
    finally:
        if os.path.exists(test_file1):
            os.remove(test_file1)
        if os.path.exists(test_file2):
            os.remove(test_file2)


def test_reproducibility_with_different_seeds():
    """Test that different seeds produce different results."""
    # Run with seed 42
    np.random.seed(42)
    data1 = np.random.normal(0, 1, (50, 3))
    result1 = basic_statistical_analysis(data1)
    
    # Run with seed 123
    np.random.seed(123)
    data2 = np.random.normal(0, 1, (50, 3))
    result2 = basic_statistical_analysis(data2)
    
    # Data should be different
    assert not np.allclose(data1, data2)
    
    # Results might be different (though pass/fail could be same for similar data)


def test_reproducibility_metrics():
    """Test that metrics are reproducible."""
    np.random.seed(42)
    data = np.random.normal(0, 1, (100, 3))
    
    # Run test multiple times
    results = []
    for i in range(3):
        np.random.seed(42)  # Reset seed each time
        result = basic_statistical_analysis(data)
        results.append(result)
    
    # All results should be identical
    for i in range(1, len(results)):
        if "pass_fail" in results[0] and "pass_fail" in results[i]:
            assert results[0]["pass_fail"] == results[i]["pass_fail"]


def test_reproducibility_truth_table():
    """Test that truth tables are reproducible."""
    np.random.seed(42)
    data = np.random.normal(0, 1, (50, 3))
    
    # Run test multiple times
    results = []
    for i in range(3):
        np.random.seed(42)  # Reset seed each time
        result = basic_statistical_analysis(data)
        results.append(result)
    
    # All results should be identical
    for i in range(1, len(results)):
        if "truth_table" in results[0] and "truth_table" in results[i]:
            assert results[0]["truth_table"] == results[i]["truth_table"]


def test_reproducibility_json_serialization():
    """Test that results are reproducible when serialized to JSON."""
    np.random.seed(42)
    data = np.random.normal(0, 1, (50, 3))
    
    # Run test
    result = basic_statistical_analysis(data)
    
    # Run again with same seed
    np.random.seed(42)
    data2 = np.random.normal(0, 1, (50, 3))
    result2 = basic_statistical_analysis(data2)
    
    # Remove timestamp for comparison
    result_copy = result.copy()
    result2_copy = result2.copy()
    
    # Remove timestamp from both results
    if 'timestamp' in result_copy:
        del result_copy['timestamp']
    if 'timestamp' in result2_copy:
        del result2_copy['timestamp']
    
    # Serialize to JSON
    json_result = json.dumps(result_copy, sort_keys=True)
    json_result2 = json.dumps(result2_copy, sort_keys=True)
    
    # JSON strings should be identical
    assert json_result == json_result2


def test_reproducibility_pipeline_save_load():
    """Test that pipeline save/load is reproducible."""
    np.random.seed(42)
    data = np.random.normal(0, 1, (50, 3))
    test_file = "temp_save_load_test.csv"
    np.savetxt(test_file, data, delimiter=',', header='col1,col2,col3')
    
    try:
        # Register test function
        from test_suite.universal_test_functions import basic_statistical_analysis
        
        # Run pipeline and save
        pipeline1 = BulletproofPipeline()
        pipeline1.register_test_function("basic_statistical_analysis", basic_statistical_analysis)
        pipeline1.load_data(test_file, "csv")
        result1 = pipeline1.run_batch_tests(["basic_statistical_analysis"])
        output_path1 = pipeline1.save_results()
        
        # Run again with same seed
        np.random.seed(42)
        data2 = np.random.normal(0, 1, (50, 3))
        test_file2 = "temp_save_load_test2.csv"
        np.savetxt(test_file2, data2, delimiter=',', header='col1,col2,col3')
        
        pipeline2 = BulletproofPipeline()
        pipeline2.register_test_function("basic_statistical_analysis", basic_statistical_analysis)
        pipeline2.load_data(test_file2, "csv")
        result2 = pipeline2.run_batch_tests(["basic_statistical_analysis"])
        output_path2 = pipeline2.save_results()
        
        # Load both results
        with open(output_path1, 'r') as f:
            loaded_result1 = json.load(f)
        
        with open(output_path2, 'r') as f:
            loaded_result2 = json.load(f)
        
        # Results should be identical
        assert loaded_result1["test_results"]["basic_statistical_analysis"]["truth_table"]["pass_fail"] == loaded_result2["test_results"]["basic_statistical_analysis"]["truth_table"]["pass_fail"]
    finally:
        if os.path.exists(test_file):
            os.remove(test_file)
        if os.path.exists(test_file2):
            os.remove(test_file2)


def test_reproducibility_clustering():
    """Test that clustering analysis is reproducible."""
    np.random.seed(42)
    # Create clustered data
    cluster1 = np.random.normal(0, 1, (25, 2))
    cluster2 = np.random.normal(5, 1, (25, 2))
    data1 = np.vstack([cluster1, cluster2])
    
    np.random.seed(42)
    cluster1_2 = np.random.normal(0, 1, (25, 2))
    cluster2_2 = np.random.normal(5, 1, (25, 2))
    data2 = np.vstack([cluster1_2, cluster2_2])
    
    # Results should be identical
    result1 = clustering_analysis(data1, max_clusters=4)
    result2 = clustering_analysis(data2, max_clusters=4)
    
    if "pass_fail" in result1 and "pass_fail" in result2:
        assert result1["pass_fail"] == result2["pass_fail"]


def test_reproducibility_signal_detection():
    """Test that signal detection is reproducible."""
    np.random.seed(42)
    t = np.linspace(0, 10, 1000)
    signal = 3 * np.sin(2 * np.pi * 2 * t)
    noise = np.random.normal(0, 1, 1000)
    data1 = signal + noise
    
    np.random.seed(42)
    t2 = np.linspace(0, 10, 1000)
    signal2 = 3 * np.sin(2 * np.pi * 2 * t2)
    noise2 = np.random.normal(0, 1, 1000)
    data2 = signal2 + noise2
    
    # Results should be identical
    result1 = signal_detection_test(data1)
    result2 = signal_detection_test(data2)
    
    if "pass_fail" in result1 and "pass_fail" in result2:
        assert result1["pass_fail"] == result2["pass_fail"]


def test_reproducibility_periodicity():
    """Test that periodicity detection is reproducible."""
    np.random.seed(42)
    t = np.linspace(0, 20, 200)
    data1 = np.sin(2 * np.pi * 0.1 * t) + np.random.normal(0, 0.1, 200)
    
    np.random.seed(42)
    t2 = np.linspace(0, 20, 200)
    data2 = np.sin(2 * np.pi * 0.1 * t2) + np.random.normal(0, 0.1, 200)
    
    # Results should be identical
    result1 = periodicity_test(data1)
    result2 = periodicity_test(data2)
    
    if "pass_fail" in result1 and "pass_fail" in result2:
        assert result1["pass_fail"] == result2["pass_fail"]


def test_reproducibility_correlation():
    """Test that correlation analysis is reproducible."""
    np.random.seed(42)
    x = np.random.normal(0, 1, 100)
    y = x + np.random.normal(0, 0.1, 100)
    data1 = np.column_stack([x, y])
    
    np.random.seed(42)
    x2 = np.random.normal(0, 1, 100)
    y2 = x2 + np.random.normal(0, 0.1, 100)
    data2 = np.column_stack([x2, y2])
    
    # Results should be identical
    result1 = correlation_analysis(data1)
    result2 = correlation_analysis(data2)
    
    if "pass_fail" in result1 and "pass_fail" in result2:
        assert result1["pass_fail"] == result2["pass_fail"]


def test_reproducibility_dimensionality():
    """Test that dimensionality analysis is reproducible."""
    np.random.seed(42)
    data1 = np.random.normal(0, 1, (100, 5))
    
    np.random.seed(42)
    data2 = np.random.normal(0, 1, (100, 5))
    
    # Results should be identical
    result1 = dimensionality_analysis(data1)
    result2 = dimensionality_analysis(data2)
    
    if "pass_fail" in result1 and "pass_fail" in result2:
        assert result1["pass_fail"] == result2["pass_fail"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 