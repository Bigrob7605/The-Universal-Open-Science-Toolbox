"""
Pipeline Smoke Tests for Universal Open Science Toolbox
=====================================================

Basic smoke tests to ensure the pipeline runs correctly with minimal data.
"""

import pytest
import numpy as np
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from BULLETPROOF_PIPELINE import BulletproofPipeline


def test_pipeline_runs_minimal():
    """Test that pipeline runs with minimal data and basic test."""
    # Create test data file
    data = np.array([[1, 2], [3, 4]])
    test_file = "temp_minimal_test.csv"
    np.savetxt(test_file, data, delimiter=',', header='col1,col2')
    
    try:
        pipeline = BulletproofPipeline()
        
        # Register the test function
        from test_suite.universal_test_functions import basic_statistical_analysis
        pipeline.register_test_function("basic_statistical_analysis", basic_statistical_analysis)
        
        # Load data and run test
        pipeline.load_data(test_file, "csv")
        report = pipeline.run_batch_tests(["basic_statistical_analysis"])
        assert "overall_truth_table" in report
        assert len(report["overall_truth_table"]["tests_run"]) > 0
    finally:
        if os.path.exists(test_file):
            os.remove(test_file)


def test_pipeline_initialization():
    """Test that pipeline can be initialized with default config."""
    pipeline = BulletproofPipeline()
    assert pipeline is not None
    assert hasattr(pipeline, 'config')
    assert hasattr(pipeline, 'test_results')
    assert hasattr(pipeline, 'log_entries')


def test_pipeline_with_config():
    """Test that pipeline can be initialized with custom config."""
    config = {"test_param": "test_value"}
    pipeline = BulletproofPipeline(config=config)
    assert pipeline.config["test_param"] == "test_value"


def test_pipeline_logging():
    """Test that pipeline logs events correctly."""
    pipeline = BulletproofPipeline()
    assert len(pipeline.log_entries) > 0  # Should have startup log
    assert any("PIPELINE_START" in entry["event_type"] for entry in pipeline.log_entries)


def test_pipeline_data_loading():
    """Test that pipeline can load simple data."""
    # Create temporary data file
    data = np.random.normal(0, 1, (10, 3))
    test_file = "temp_pipeline_data.csv"
    np.savetxt(test_file, data, delimiter=',', header='col1,col2,col3')
    
    try:
        pipeline = BulletproofPipeline()
        success = pipeline.load_data(test_file, "csv")
        assert success
        assert hasattr(pipeline, 'data')
        assert pipeline.data is not None
    finally:
        if os.path.exists(test_file):
            os.remove(test_file)


def test_pipeline_test_registration():
    """Test that custom tests can be registered."""
    pipeline = BulletproofPipeline()
    
    def custom_test(data, **kwargs):
        return {"custom_metric": 42.0, "pass_fail": {"test_passed": True}}
    
    pipeline.register_test_function("custom_test", custom_test)
    assert "custom_test" in pipeline.test_functions


def test_pipeline_save_results():
    """Test that pipeline can save results."""
    # Create test data file
    data = np.array([[1, 2], [3, 4]])
    test_file = "temp_save_test.csv"
    np.savetxt(test_file, data, delimiter=',', header='col1,col2')
    
    try:
        pipeline = BulletproofPipeline()
        
        # Register the test function
        from test_suite.universal_test_functions import basic_statistical_analysis
        pipeline.register_test_function("basic_statistical_analysis", basic_statistical_analysis)
        
        # Load data and run test
        pipeline.load_data(test_file, "csv")
        pipeline.run_batch_tests(["basic_statistical_analysis"])
        
        # Test saving results
        output_path = pipeline.save_results()
        assert output_path is not None
        assert os.path.exists(output_path)
    finally:
        if os.path.exists(test_file):
            os.remove(test_file)


def test_pipeline_generate_report():
    """Test that pipeline can generate reports."""
    # Create test data file
    data = np.array([[1, 2], [3, 4]])
    test_file = "temp_report_test.csv"
    np.savetxt(test_file, data, delimiter=',', header='col1,col2')
    
    try:
        pipeline = BulletproofPipeline()
        
        # Register the test function
        from test_suite.universal_test_functions import basic_statistical_analysis
        pipeline.register_test_function("basic_statistical_analysis", basic_statistical_analysis)
        
        # Load data and run test
        pipeline.load_data(test_file, "csv")
        pipeline.run_batch_tests(["basic_statistical_analysis"])
        
        # Test generating report
        report_path = pipeline.generate_report()
        assert report_path is not None
        assert os.path.exists(report_path)
    finally:
        if os.path.exists(test_file):
            os.remove(test_file)


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 