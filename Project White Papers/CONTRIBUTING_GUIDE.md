# Contributing Guide - Universal Open Science Toolbox

**How to Contribute to Bulletproof Scientific Testing**

## 🎯 Welcome Contributors!

The Universal Open Science Toolbox is built on the principle that **open science works**. We welcome contributions from researchers, developers, students, and citizen scientists who want to make scientific testing more robust, transparent, and accessible.

**RIFE is dead. Long live open science.**

## 📋 Table of Contents

1. [Getting Started](#getting-started)
2. [Types of Contributions](#types-of-contributions)
3. [Development Setup](#development-setup)
4. [Adding New Test Functions](#adding-new-test-functions)
5. [Adding New Data Sources](#adding-new-data-sources)
6. [Improving Documentation](#improving-documentation)
7. [Code Style and Standards](#code-style-and-standards)
8. [Testing Your Contributions](#testing-your-contributions)
9. [Submitting Your Contribution](#submitting-your-contribution)
10. [Community Guidelines](#community-guidelines)

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Basic knowledge of scientific computing
- Understanding of open science principles
- Git and GitHub account

### Quick Start

1. **Fork the repository**
   ```bash
   git clone https://github.com/your-username/universal-open-science-toolbox.git
   cd universal-open-science-toolbox
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements_universal.txt
   ```

3. **Run the basic example**
   ```bash
   python examples/basic_example.py
   ```

4. **Verify everything works**
   ```bash
   python BULLETPROOF_PIPELINE.py --input=test_data_iris.csv --test=basic_statistical_analysis
   ```

## 🔧 Types of Contributions

### 1. New Test Functions

Add new analysis functions to `test_suite/universal_test_functions.py`:

- **Statistical tests** (new statistical methods)
- **Signal processing** (new detection algorithms)
- **Machine learning** (new clustering/classification methods)
- **Domain-specific tests** (physics, biology, climate, seismology, etc.)

### 2. New Data Sources

Add new datasets to `download_public_data.py`:

- **Scientific datasets** (astronomy, physics, biology, etc.)
- **Public repositories** (government data, academic datasets)
- **Real-time data** (APIs, streaming sources)

### 3. Documentation Improvements

- **Tutorials** and examples
- **API documentation** updates
- **User guides** for specific domains
- **Translation** to other languages

### 4. Framework Enhancements

- **Performance improvements**
- **New data formats** support
- **Additional output formats**
- **Web interface** development

### 5. Bug Fixes and Maintenance

- **Error handling** improvements
- **Compatibility** updates
- **Security** enhancements
- **Code optimization**

## 🛠️ Development Setup

### Environment Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements_universal.txt

# Install development dependencies
pip install pytest black flake8 mypy
```

### Project Structure

```
Universal Open Science Toolbox/
├── BULLETPROOF_PIPELINE.py              # Main framework
├── download_public_data.py               # Data downloader
├── test_suite/
│   └── universal_test_functions.py       # Test functions
├── docs/
│   └── README.md                        # Documentation
├── examples/
│   └── basic_example.py                 # Examples
├── tests/                               # Unit tests (to be added)
├── requirements_universal.txt            # Dependencies
└── [other files...]
```

### Running Tests

```bash
# Run basic example
python examples/basic_example.py

# Run specific test
python BULLETPROOF_PIPELINE.py --input=test_data_iris.csv --test=basic_statistical_analysis

# Run with verbose output
python BULLETPROOF_PIPELINE.py --input=test_data_iris.csv --verbose
```

## 🔬 Adding New Test Functions

### Template for New Test Functions

```python
def your_new_test_function(data: np.ndarray, **kwargs) -> Dict[str, Any]:
    """
    Your new analysis function.
    
    Parameters:
    -----------
    data : np.ndarray
        Input data array
    **kwargs : Additional parameters
        - param1 : Description of parameter 1
        - param2 : Description of parameter 2
        
    Returns:
    --------
    dict : Analysis results with the following structure:
        {
            "metric1": value1,
            "metric2": value2,
            "threshold_test": bool,
            "custom_analysis": {...}
        }
    """
    try:
        # Your analysis code here
        result = {
            "metric1": 42.0,
            "metric2": 3.14,
            "threshold_test": True,
            "custom_analysis": {
                "detail1": "value1",
                "detail2": "value2"
            }
        }
        
        return result
        
    except Exception as e:
        return {"error": f"Analysis failed: {str(e)}"}
```

### Example: Adding a New Statistical Test

```python
def robust_statistics_test(data: np.ndarray, **kwargs) -> Dict[str, Any]:
    """
    Robust statistical analysis using median-based methods.
    
    Parameters:
    -----------
    data : np.ndarray
        Input data array
    **kwargs : Additional parameters
        - method : Robust method ('median', 'trimmed', 'winsorized')
        
    Returns:
    --------
    dict : Robust statistics results
    """
    try:
        from scipy import stats
        
        # Ensure data is 2D
        if data.ndim == 1:
            data_2d = data.reshape(-1, 1)
        else:
            data_2d = data
        
        method = kwargs.get('method', 'median')
        
        results = {}
        
        if method == 'median':
            # Median-based statistics
            results['median'] = np.median(data_2d, axis=0).tolist()
            results['mad'] = stats.median_abs_deviation(data_2d, axis=0).tolist()
            
        elif method == 'trimmed':
            # Trimmed mean statistics
            results['trimmed_mean'] = stats.trim_mean(data_2d, 0.1, axis=0).tolist()
            results['trimmed_std'] = stats.tstd(data_2d, axis=0).tolist()
            
        elif method == 'winsorized':
            # Winsorized statistics
            results['winsorized_mean'] = stats.mstats.winsorize(data_2d, limits=[0.1, 0.1]).mean(axis=0).tolist()
            results['winsorized_std'] = stats.mstats.winsorize(data_2d, limits=[0.1, 0.1]).std(axis=0).tolist()
        
        # Add method information
        results['method'] = method
        results['data_shape'] = data_2d.shape
        
        return results
        
    except Exception as e:
        return {"error": f"Robust statistics test failed: {str(e)}"}
```

### Registering Your New Test

```python
# In your script or example
from test_suite.universal_test_functions import robust_statistics_test

# Register the new test
pipeline.register_test_function("robust_statistics", robust_statistics_test)

# Run the new test
result = pipeline.run_test("robust_statistics", method="median")
```

## 📊 Adding New Data Sources

### Template for New Dataset

```python
# Add to PUBLIC_DATASETS in download_public_data.py
"your_dataset_name": {
    "url": "https://example.com/your_dataset.csv",
    "description": "Description of your dataset",
    "format": "csv",
    "size_estimate": "1MB",
    "category": "your_category"
}
```

### Example: Adding a New Astronomy Dataset

```python
"gaia_stars": {
    "url": "https://gea.esac.esa.int/data-server/data?RETRIEVAL_TYPE=EPOCH_PHOTOMETRY&ID=5853498713190525696&FORMAT=CSV",
    "description": "Gaia DR3 star photometry data",
    "format": "csv",
    "size_estimate": "5MB",
    "category": "astronomy"
}
```

### Testing Your New Data Source

```python
# Test the download
python download_public_data.py --dataset=your_dataset_name

# Verify the download
python download_public_data.py --verify=your_dataset_name

# Use in pipeline
python BULLETPROOF_PIPELINE.py --input=data/your_dataset_name.csv --test=basic_statistical_analysis
```

## 📚 Improving Documentation

### Documentation Standards

1. **Clear and concise** explanations
2. **Complete examples** with expected outputs
3. **Cross-references** to related documentation
4. **Regular updates** as code changes

### Types of Documentation

#### 1. Function Documentation

```python
def your_function(data, **kwargs):
    """
    Brief description of what the function does.
    
    Parameters:
    -----------
    data : np.ndarray
        Input data array with shape (n_samples, n_features)
    **kwargs : Additional parameters
        - param1 : Description and default value
        - param2 : Description and default value
        
    Returns:
    --------
    dict : Results dictionary with the following keys:
        - key1 : Description of key1
        - key2 : Description of key2
        
    Examples:
    --------
    >>> result = your_function(data, param1=5.0)
    >>> print(result['key1'])
    42.0
    
    Notes:
    -----
    Additional notes about implementation, limitations, etc.
    """
```

#### 2. Example Documentation

```markdown
## Example: Your Analysis

**Domain**: Your scientific domain  
**Data**: Description of your data  
**Goal**: What you're trying to achieve

### Code
```python
# Your complete example code
```

### Expected Output
```json
{
  "expected": "output structure"
}
```

### Key Features Demonstrated
- ✅ Feature 1
- ✅ Feature 2
- ✅ Feature 3
```

#### 3. Tutorial Documentation

```markdown
# Tutorial: Your Topic

## Overview
Brief introduction to the topic.

## Prerequisites
What users need to know before starting.

## Step-by-Step Guide

### Step 1: Setup
```bash
# Commands to run
```

### Step 2: Analysis
```python
# Code to run
```

### Step 3: Results
Explanation of results and interpretation.

## Next Steps
What users can do next.
```

## 🎨 Code Style and Standards

### Python Style Guide

Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) with these additions:

```python
# Good
def calculate_statistics(data: np.ndarray, threshold: float = 5.0) -> Dict[str, Any]:
    """Calculate statistical measures for the dataset."""
    result = {
        "mean": np.mean(data),
        "std": np.std(data),
        "threshold_test": np.mean(data) > threshold
    }
    return result

# Bad
def calc_stats(d, t=5.0):
    """Calculate stats."""
    r = {"mean": np.mean(d), "std": np.std(d), "test": np.mean(d) > t}
    return r
```

### Naming Conventions

- **Functions**: `snake_case` (e.g., `basic_statistical_analysis`)
- **Classes**: `PascalCase` (e.g., `BulletproofPipeline`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `DEFAULT_TIMEOUT`)
- **Files**: `snake_case` (e.g., `universal_test_functions.py`)

### Documentation Standards

- **Docstrings**: Use Google or NumPy style
- **Type hints**: Include for all functions
- **Examples**: Provide working examples
- **Error handling**: Document expected exceptions

### Error Handling

```python
def robust_function(data: np.ndarray, **kwargs) -> Dict[str, Any]:
    """Robust function with proper error handling."""
    try:
        # Your analysis code
        result = perform_analysis(data, **kwargs)
        return result
        
    except ValueError as e:
        return {"error": f"Invalid input: {str(e)}"}
        
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}
```

## 🧪 Testing Your Contributions

### Unit Testing

Create tests for your new functions:

```python
# tests/test_your_function.py
import numpy as np
import pytest
from test_suite.universal_test_functions import your_new_function

def test_your_new_function():
    """Test your new function with known data."""
    # Create test data
    test_data = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    
    # Run your function
    result = your_new_function(test_data)
    
    # Assert expected results
    assert "metric1" in result
    assert isinstance(result["metric1"], (int, float))
    assert "error" not in result

def test_your_new_function_error_handling():
    """Test error handling in your function."""
    # Test with invalid input
    result = your_new_function(None)
    
    # Assert error is properly handled
    assert "error" in result
    assert "failed" in result["error"].lower()
```

### Integration Testing

Test your function with the pipeline:

```python
# test_integration.py
from BULLETPROOF_PIPELINE import BulletproofPipeline
from test_suite.universal_test_functions import your_new_function

def test_pipeline_integration():
    """Test your function integrated with the pipeline."""
    # Initialize pipeline
    pipeline = BulletproofPipeline()
    
    # Load test data
    success = pipeline.load_data("test_data_iris.csv", "csv")
    assert success
    
    # Register your function
    pipeline.register_test_function("your_test", your_new_function)
    
    # Run test
    result = pipeline.run_test("your_test")
    
    # Assert results
    assert "truth_table" in result
    assert "error" not in result
```

### Manual Testing

```bash
# Test your new function
python -c "
from BULLETPROOF_PIPELINE import BulletproofPipeline
from test_suite.universal_test_functions import your_new_function
import numpy as np

pipeline = BulletproofPipeline()
pipeline.load_data('test_data_iris.csv', 'csv')
pipeline.register_test_function('your_test', your_new_function)
result = pipeline.run_test('your_test')
print('Success!' if 'error' not in result else 'Failed')
"
```

## 📤 Submitting Your Contribution

### 1. Fork and Clone

```bash
git clone https://github.com/your-username/universal-open-science-toolbox.git
cd universal-open-science-toolbox
```

### 2. Create a Branch

```bash
git checkout -b feature/your-new-feature
# or
git checkout -b fix/your-bug-fix
```

### 3. Make Your Changes

- Add your new code
- Update documentation
- Add tests
- Update examples if needed

### 4. Test Your Changes

```bash
# Run basic tests
python examples/basic_example.py

# Test your specific changes
python BULLETPROOF_PIPELINE.py --input=test_data_iris.csv --test=your_new_test

# Run any new examples
python your_new_example.py
```

### 5. Commit Your Changes

```bash
git add .
git commit -m "Add new statistical test function

- Added robust_statistics_test function
- Includes median, trimmed mean, and winsorized statistics
- Added comprehensive documentation and examples
- Includes error handling for edge cases

Closes #123"
```

### 6. Push and Create Pull Request

```bash
git push origin feature/your-new-feature
```

Then create a pull request on GitHub with:

- **Clear title** describing your contribution
- **Detailed description** of what you changed and why
- **Examples** of how to use your new feature
- **Tests** showing your code works
- **Documentation** updates

### 7. Pull Request Template

```markdown
## Description
Brief description of your contribution.

## Type of Change
- [ ] New feature (non-breaking change)
- [ ] Bug fix (non-breaking change)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing
- [ ] Added unit tests for new functionality
- [ ] All existing tests pass
- [ ] Manual testing completed
- [ ] Examples updated

## Documentation
- [ ] Updated function docstrings
- [ ] Updated README files
- [ ] Added examples
- [ ] Updated API reference

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Code is well documented
- [ ] No new warnings generated
```

## 🤝 Community Guidelines

### Code of Conduct

We are committed to providing a welcoming and inspiring community for all. Please:

- **Be respectful** and inclusive
- **Help others** learn and grow
- **Give credit** where credit is due
- **Be constructive** in feedback
- **Follow scientific** best practices

### Communication Channels

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and community chat
- **Pull Requests**: Code contributions and reviews
- **Documentation**: Help improve guides and tutorials

### Recognition

Contributors will be recognized in:

- **README.md** contributor list
- **Release notes** for significant contributions
- **Documentation** credits
- **Community** acknowledgments

### Mentorship

New contributors can:

- **Ask questions** in GitHub Discussions
- **Request reviews** from experienced contributors
- **Join community** events and workshops
- **Learn from** existing examples and documentation

## 🎯 Getting Help

### Before Asking

1. **Check existing documentation**
2. **Search GitHub issues** for similar problems
3. **Try the examples** in the repository
4. **Read the API reference**

### When Asking for Help

Provide:

- **Clear description** of what you're trying to do
- **Minimal example** that reproduces the issue
- **Error messages** (if any)
- **Your environment** (Python version, OS, etc.)
- **What you've tried** already

### Example Help Request

```markdown
## Issue Description
I'm trying to add a new statistical test function but getting an error.

## Code Example
```python
def my_test(data, **kwargs):
    return {"metric": np.mean(data)}

pipeline.register_test_function("my_test", my_test)
result = pipeline.run_test("my_test")
```

## Error Message
```
TypeError: 'NoneType' object is not subscriptable
```

## Environment
- Python 3.9.7
- Windows 10
- Universal Open Science Toolbox v1.0

## What I've Tried
- Checked that data is loaded correctly
- Verified function signature matches template
- Tried with different datasets
```

## 🚀 Advanced Contributing

### Framework Extensions

For advanced contributors:

1. **New pipeline features** (parallel processing, distributed computing)
2. **Web interface** development
3. **Plugin system** for custom analysis
4. **Cloud integration** for large-scale processing
5. **Educational tools** and tutorials

### Research Contributions

We welcome:

- **New statistical methods** and algorithms
- **Domain-specific** analysis functions
- **Performance optimizations** for large datasets
- **Reproducibility** enhancements
- **Open science** methodology improvements

### Documentation Contributions

Help with:

- **Translation** to other languages
- **Video tutorials** and screencasts
- **Interactive examples** and notebooks
- **Case studies** from real research
- **Best practices** guides

---

**RIFE is dead. Long live open science.**

*"This framework was forged in the fire of RIFE—a theory we put to the sword on real data, no excuses, and left for the world to audit. The code survived, even when the theory died. Now, anyone can plug in any new hypothesis, any field, and run the same bulletproof, tamper-proof, open science test—at home, for free, with receipts."*

**Thank you for contributing to the future of open science!** 🌍🔬✨ 