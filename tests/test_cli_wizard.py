"""
CLI Wizard Functional Tests
==========================

Tests for CLI wizard functionality and command-line interface.
"""

import pytest
import subprocess
import sys
import os
import tempfile
import json

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cli_wizard import UniversalScienceWizard


def test_cli_list_tests():
    """Test that CLI lists available tests."""
    result = subprocess.run(
        ["python", "cli_wizard.py", "--list-tests"], 
        capture_output=True, 
        text=True
    )
    assert result.returncode == 0
    assert "Available Tests" in result.stdout or "basic_statistical_analysis" in result.stdout


def test_cli_wizard_import():
    """Test that CLI wizard can be imported."""
    wizard = UniversalScienceWizard()
    assert wizard is not None
    assert hasattr(wizard, 'pipeline')
    assert hasattr(wizard, 'downloader')
    assert hasattr(wizard, 'available_tests')


def test_cli_wizard_banner():
    """Test that wizard banner prints correctly."""
    wizard = UniversalScienceWizard()
    
    # Capture stdout
    import io
    from contextlib import redirect_stdout
    
    f = io.StringIO()
    with redirect_stdout(f):
        wizard.print_banner()
    
    output = f.getvalue()
    assert "Universal Open Science Toolbox" in output
    assert "CLI Wizard" in output


def test_cli_wizard_available_tests():
    """Test that wizard has access to available tests."""
    wizard = UniversalScienceWizard()
    assert wizard.available_tests is not None
    assert isinstance(wizard.available_tests, dict)
    assert len(wizard.available_tests) > 0


def test_cli_wizard_pipeline_initialization():
    """Test that wizard initializes pipeline correctly."""
    wizard = UniversalScienceWizard()
    assert wizard.pipeline is not None
    assert hasattr(wizard.pipeline, 'load_data')
    assert hasattr(wizard.pipeline, 'run_test')


def test_cli_wizard_downloader_initialization():
    """Test that wizard initializes downloader correctly."""
    wizard = UniversalScienceWizard()
    assert wizard.downloader is not None
    assert hasattr(wizard.downloader, 'download_dataset')


def test_cli_help():
    """Test that CLI shows help information."""
    result = subprocess.run(
        ["python", "cli_wizard.py", "--help"], 
        capture_output=True, 
        text=True
    )
    assert result.returncode == 0
    assert "help" in result.stdout.lower() or "usage" in result.stdout.lower()


def test_cli_version():
    """Test that CLI shows version information."""
    result = subprocess.run(
        ["python", "cli_wizard.py", "--version"], 
        capture_output=True, 
        text=True
    )
    # Should either show version or help
    assert result.returncode == 0 or result.returncode == 2


def test_cli_invalid_argument():
    """Test that CLI handles invalid arguments gracefully."""
    result = subprocess.run(
        ["python", "cli_wizard.py", "--invalid-arg"], 
        capture_output=True, 
        text=True
    )
    # Should not crash, should show error or help
    assert result.returncode != 0 or "error" in result.stderr.lower() or "help" in result.stdout.lower()


def test_cli_wizard_test_selection():
    """Test that wizard can select tests."""
    wizard = UniversalScienceWizard()
    
    # Test that available tests are accessible
    tests = wizard.available_tests
    assert isinstance(tests, dict)
    
    # Test that at least one test is available
    assert len(tests) > 0
    
    # Test that test names are strings
    for test_name in tests.keys():
        assert isinstance(test_name, str)


def test_cli_wizard_data_selection():
    """Test that wizard can handle data selection."""
    wizard = UniversalScienceWizard()
    
    # Test with existing test file
    if os.path.exists("test_data_iris.csv"):
        # This would normally be interactive, but we can test the method exists
        assert hasattr(wizard, 'select_data')
        assert hasattr(wizard, 'select_existing_file')


def test_cli_wizard_run_test():
    """Test that wizard can run tests."""
    wizard = UniversalScienceWizard()
    
    # Test with sample data
    if os.path.exists("test_data_iris.csv"):
        result = wizard.run_test("test_data_iris.csv", "basic_statistical_analysis")
        assert result is not None
        assert isinstance(result, dict)


def test_cli_wizard_save_results():
    """Test that wizard can save results."""
    wizard = UniversalScienceWizard()
    
    # Create sample result
    sample_result = {
        "test_name": "basic_statistical_analysis",
        "timestamp": "2024-01-01T00:00:00",
        "pass_fail": {"test_passed": True},
        "metrics": {"mean": 0.0, "std": 1.0}
    }
    
    # Test saving results
    wizard.save_results(sample_result)
    # Should not raise an exception


def test_cli_wizard_show_results():
    """Test that wizard can show results."""
    wizard = UniversalScienceWizard()
    
    # Create sample result
    sample_result = {
        "test_name": "basic_statistical_analysis",
        "timestamp": "2024-01-01T00:00:00",
        "pass_fail": {"test_passed": True},
        "metrics": {"mean": 0.0, "std": 1.0}
    }
    
    # Test showing results (should not crash)
    wizard.show_results(sample_result)


def test_cli_command_line_mode():
    """Test that CLI can run in command line mode."""
    wizard = UniversalScienceWizard()
    
    # Test that command line mode method exists
    assert hasattr(wizard, 'command_line_mode')


def test_cli_list_available_datasets():
    """Test that CLI can list available datasets."""
    wizard = UniversalScienceWizard()
    
    # Test that method exists
    assert hasattr(wizard, 'list_available_datasets')


def test_cli_download_sample_data():
    """Test that CLI can download sample data."""
    wizard = UniversalScienceWizard()
    
    # Test that method exists
    assert hasattr(wizard, 'download_sample_data')


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 