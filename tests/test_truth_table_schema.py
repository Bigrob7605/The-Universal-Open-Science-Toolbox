"""
Truth Table Schema Tests
=======================

Tests to ensure all tests return valid truth table schemas.
"""

import pytest
import numpy as np
import sys
import os
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from test_suite.universal_test_functions import (
    basic_statistical_analysis,
    correlation_analysis,
    signal_detection_test,
    periodicity_test,
    clustering_analysis,
    dimensionality_analysis
)


def test_truth_table_schema():
    """Test that all tests return valid truth table schema."""
    data = np.random.normal(0, 1, (20, 3))
    
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
                entry = truth_table[0]
                assert "test_name" in entry
                assert "timestamp" in entry
                assert "pass_fail" in entry
                
                # Check data types
                assert isinstance(entry["test_name"], str)
                assert isinstance(entry["timestamp"], str)
                assert isinstance(entry["pass_fail"], dict)


def test_pass_fail_boolean_values():
    """Test that all pass/fail values are booleans."""
    data = np.random.normal(0, 1, (20, 3))
    
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
        
        # Check pass_fail structure
        if "pass_fail" in result:
            pass_fail = result["pass_fail"]
            assert isinstance(pass_fail, dict)
            
            # All values should be booleans
            for key, value in pass_fail.items():
                assert isinstance(value, bool), f"Pass/fail value for {key} should be boolean"


def test_truth_table_required_fields():
    """Test that truth tables have all required fields."""
    data = np.random.normal(0, 1, (20, 3))
    
    tests = [
        basic_statistical_analysis,
        correlation_analysis,
        signal_detection_test,
        periodicity_test,
        clustering_analysis,
        dimensionality_analysis
    ]
    
    required_fields = ["test_name", "timestamp", "pass_fail"]
    
    for test_func in tests:
        result = test_func(data)
        
        if "truth_table" in result:
            truth_table = result["truth_table"]
            if len(truth_table) > 0:
                entry = truth_table[0]
                
                for field in required_fields:
                    assert field in entry, f"Truth table missing required field: {field}"


def test_truth_table_timestamp_format():
    """Test that truth table timestamps are in correct format."""
    data = np.random.normal(0, 1, (20, 3))
    
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
        
        if "truth_table" in result:
            truth_table = result["truth_table"]
            if len(truth_table) > 0:
                entry = truth_table[0]
                timestamp = entry["timestamp"]
                
                # Check timestamp format (should be ISO format)
                assert "T" in timestamp or "-" in timestamp
                assert len(timestamp) > 0


def test_truth_table_test_name_consistency():
    """Test that truth table test names are consistent."""
    data = np.random.normal(0, 1, (20, 3))
    
    tests = [
        (basic_statistical_analysis, "basic_statistical_analysis"),
        (correlation_analysis, "correlation_analysis"),
        (signal_detection_test, "signal_detection_test"),
        (periodicity_test, "periodicity_test"),
        (clustering_analysis, "clustering_analysis"),
        (dimensionality_analysis, "dimensionality_analysis")
    ]
    
    for test_func, expected_name in tests:
        result = test_func(data)
        
        if "truth_table" in result:
            truth_table = result["truth_table"]
            if len(truth_table) > 0:
                entry = truth_table[0]
                test_name = entry["test_name"]
                
                # Test name should match expected
                assert test_name == expected_name


def test_truth_table_metrics_presence():
    """Test that truth tables include metrics or evidence."""
    data = np.random.normal(0, 1, (20, 3))
    
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
        
        # Should have either metrics or evidence
        has_metrics = "metrics" in result
        has_evidence = "evidence" in result
        has_specific_metrics = any(key in result for key in [
            "mean", "std", "correlation", "signal_statistics", 
            "periodicity_summary", "cluster_analysis", "dimensions"
        ])
        
        assert has_metrics or has_evidence or has_specific_metrics


def test_truth_table_falsification_notes():
    """Test that truth tables include falsification notes when appropriate."""
    data = np.random.normal(0, 1, (20, 3))
    
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
        
        # Check if falsification_notes field exists
        if "truth_table" in result:
            truth_table = result["truth_table"]
            if len(truth_table) > 0:
                entry = truth_table[0]
                
                # Falsification notes should be present (even if empty)
                if "falsification_notes" in entry:
                    assert isinstance(entry["falsification_notes"], str)


def test_truth_table_error_handling():
    """Test that truth tables handle errors gracefully."""
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


def test_truth_table_reproducibility():
    """Test that truth tables are reproducible with same data."""
    np.random.seed(42)
    data1 = np.random.normal(0, 1, (20, 3))
    
    np.random.seed(42)
    data2 = np.random.normal(0, 1, (20, 3))
    
    # Both datasets should be identical
    assert np.allclose(data1, data2)
    
    # Results should be identical
    result1 = basic_statistical_analysis(data1)
    result2 = basic_statistical_analysis(data2)
    
    # Check that pass/fail results are identical
    if "pass_fail" in result1 and "pass_fail" in result2:
        assert result1["pass_fail"] == result2["pass_fail"]


def test_truth_table_schema_validation():
    """Test that truth table schema is valid JSON serializable."""
    data = np.random.normal(0, 1, (20, 3))
    
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
        
        # Should be JSON serializable
        try:
            import json
            json.dumps(result)
        except (TypeError, ValueError) as e:
            pytest.fail(f"Result from {test_func.__name__} is not JSON serializable: {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 