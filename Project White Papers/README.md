# Universal Open Science Toolbox

**Born from the live-fire testing and honest falsification of RIFE 28.0, this toolkit is a plug-and-play pipeline for bulletproof scientific truth-testing.**

Use it to test *anything*—physics, bio, climate, social data. Truth is what survives.

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements_universal.txt

# Download sample data
python download_public_data.py --dataset=iris

# Run your first test
python BULLETPROOF_PIPELINE.py --input=data/iris.csv --test=basic_statistical_analysis

# Run all tests on a dataset
python BULLETPROOF_PIPELINE.py --input=data/iris.csv --auto-detect
```

## 📖 The Story

This framework was forged in the fire of RIFE—a theory we put to the sword on real data, no excuses, and left for the world to audit. The code survived, even when the theory died.

**RIFE is dead. Long live open science.**

Now, anyone can plug in any new hypothesis, any field, and run the same bulletproof, tamper-proof, open science test—at home, for free, with receipts.

## 🔧 What You Get

### 1. **Bulletproof Pipeline** (`BULLETPROOF_PIPELINE.py`)
- **Universal data loading** (CSV, HDF5, FITS, NumPy arrays)
- **Bulletproof error handling** (never crashes on bad data)
- **Comprehensive logging** (every step, input, output)
- **Truth table generation** (pass/fail matrix for any hypothesis)
- **Batch processing** (multiple files, auto-detection)

### 2. **Data Downloader** (`download_public_data.py`)
- **Multiple data sources** (astronomy, physics, climate, social sciences)
- **Automatic manifest generation** (file hashes, metadata)
- **Graceful error handling** (404 fallback, timeouts)
- **Verification tools** (check file integrity)

### 3. **Universal Test Suite** (`test_suite/universal_test_functions.py`)
- **Statistical analysis** (mean, std, normality, outliers)
- **Correlation analysis** (Pearson, Spearman, significance)
- **Signal processing** (peak detection, FFT, periodicity)
- **Machine learning** (clustering, dimensionality analysis)
- **Custom test template** (add your own analysis)

## 🎯 How to Use

### Basic Usage

```python
from BULLETPROOF_PIPELINE import BulletproofPipeline
from test_suite.universal_test_functions import basic_statistical_analysis

# Initialize pipeline
pipeline = BulletproofPipeline()

# Load data
pipeline.load_data("your_data.csv")

# Register and run a test
pipeline.register_test_function("statistical_test", basic_statistical_analysis)
result = pipeline.run_test("statistical_test")

# Save results
pipeline.save_results("my_results.json")
pipeline.generate_report("my_report.md")
```

### Command Line Interface

```bash
# Single file analysis
python BULLETPROOF_PIPELINE.py --input=data.csv --test=basic_statistical_analysis

# Batch processing
python BULLETPROOF_PIPELINE.py --input=/data/ --batch --output=results.json

# Auto-detect data type
python BULLETPROOF_PIPELINE.py --input=data.hdf5 --auto-detect

# Verbose output
python BULLETPROOF_PIPELINE.py --input=data.csv --verbose
```

### Adding Custom Tests

```python
def my_custom_test(data, **kwargs):
    """Your custom analysis function"""
    # Your analysis here
    return {
        "custom_metric": 42.0,
        "threshold": kwargs.get("threshold", 5.0),
        "test_passed": True
    }

# Register your test
pipeline.register_test_function("my_test", my_custom_test)

# Run your test
result = pipeline.run_test("my_test", threshold=3.0)
```

## 📊 Available Tests

### Statistical Tests
- **`basic_statistical_analysis`**: Mean, std, normality, outliers
- **`correlation_analysis`**: Pearson/Spearman correlations, significance

### Signal Processing Tests
- **`signal_detection_test`**: Peak detection, SNR, frequency analysis
- **`periodicity_test`**: Autocorrelation, FFT-based periodicity

### Machine Learning Tests
- **`clustering_analysis`**: K-means clustering with optimal k selection
- **`dimensionality_analysis`**: Variance analysis, correlation structure

## 📋 Data Formats Supported

### Input Formats
- **CSV**: Comma-separated values
- **HDF5**: Hierarchical data format
- **FITS**: Astronomical data format
- **NumPy**: `.npy` and `.npz` files
- **Generic**: Any format NumPy can load

### Output Formats
- **JSON**: Comprehensive results with metadata
- **Markdown**: Human-readable reports
- **Logs**: Detailed execution logs

## 🔍 Truth Table Generation

Every test generates a truth table with:

```json
{
  "test_name": "basic_statistical_analysis",
  "timestamp": "2024-01-01T12:00:00",
  "pass_fail": {
    "snr_threshold": true,
    "statistical_significance": false,
    "detection": true
  },
  "metrics": {
    "snr": 6.2,
    "p_value": 0.03,
    "mean": 5.4
  },
  "summary": "Pass rate: 66.7% (2/3)"
}
```

## 🛡️ Bulletproof Features

### Error Handling
- **Never crashes** on bad data
- **Graceful degradation** when files are missing
- **Comprehensive error logging** with context
- **Automatic recovery** from network issues

### Reproducibility
- **Data hashing** for exact reproducibility
- **Random seed control** for stochastic tests
- **Environment logging** (Python version, dependencies)
- **Complete provenance** tracking

### Scalability
- **Handles millions of records** efficiently
- **Memory-optimized** for large datasets
- **Parallel processing** support
- **Progress tracking** for long runs

## 📈 Example Workflows

### 1. Astronomy Data Analysis

```bash
# Download astronomical data
python download_public_data.py --dataset=ligo_sample

# Analyze for gravitational wave signals
python BULLETPROOF_PIPELINE.py --input=data/ligo_sample.json --test=signal_detection_test

# Check for periodic patterns
python BULLETPROOF_PIPELINE.py --input=data/ligo_sample.json --test=periodicity_test
```

### 2. Climate Data Analysis

```bash
# Download climate data
python download_public_data.py --dataset=noaa_temperature

# Analyze temperature trends
python BULLETPROOF_PIPELINE.py --input=data/noaa_temperature.csv --test=basic_statistical_analysis

# Check for seasonal patterns
python BULLETPROOF_PIPELINE.py --input=data/noaa_temperature.csv --test=periodicity_test
```

### 3. Social Science Data

```bash
# Download social data
python download_public_data.py --dataset=gapminder

# Analyze correlations
python BULLETPROOF_PIPELINE.py --input=data/gapminder.tsv --test=correlation_analysis

# Check for clustering patterns
python BULLETPROOF_PIPELINE.py --input=data/gapminder.tsv --test=clustering_analysis
```

## 🔬 Scientific Rigor

### Falsification Contract
Every test includes:
- **Pre-defined success criteria**
- **Statistical significance thresholds**
- **Systematic error budgets**
- **Retraction protocols**

### Open Science Principles
- **Complete transparency** (all code, data, results)
- **Reproducible workflows** (one command to replicate)
- **No black boxes** (every step documented)
- **Community verification** (invite others to break your results)

## 🚨 Troubleshooting

### Common Issues

**Data loading fails:**
```bash
# Check file format
python BULLETPROOF_PIPELINE.py --input=data.csv --verbose

# Try auto-detection
python BULLETPROOF_PIPELINE.py --input=data.csv --auto-detect
```

**Test not found:**
```bash
# List available tests
python BULLETPROOF_PIPELINE.py --help

# Check test registration
python -c "from test_suite.universal_test_functions import get_available_tests; print(get_available_tests())"
```

**Memory issues:**
```bash
# Use smaller datasets for testing
python download_public_data.py --dataset=iris

# Process in chunks
python BULLETPROOF_PIPELINE.py --input=data.csv --config=config_small.json
```

## 📞 Community & Support

### Getting Help
- **Documentation**: See `GETTING_STARTED.md` for detailed guides
- **Examples**: See `EXAMPLES_GALLERY.md` for tutorials
- **API Reference**: See `API_REFERENCE.md` for technical details
- **Contributing**: See `CONTRIBUTING_GUIDE.md` for development guidelines

### Contributing
1. **Fork the repository**
2. **Add your test function** to `test_suite/`
3. **Update documentation** with examples
4. **Submit a pull request**

### Citation
If you use this toolbox in your research:

```bibtex
@software{universal_open_science_toolbox,
  title={Universal Open Science Toolbox},
  author={Open Science Community},
  year={2024},
  url={https://github.com/your-repo/universal-open-science-toolbox}
}
```

## 🎯 What Makes This Special

### Born from Real Science
This framework was forged in the fire of RIFE—a theory we put to the sword on real data, no excuses, and left for the world to audit. The code survived, even when the theory died.

### Universal Applicability
- **Any field**: Physics, biology, climate, seismology, social sciences
- **Any data**: Time series, images, tabular, signals
- **Any hypothesis**: Drop in your model, get truth table
- **Any scale**: From laptop to supercomputer

### Bulletproof Design
- **Never crashes** on bad data
- **Complete audit trail** for every result
- **Reproducible by anyone** with one command
- **Open to verification** by the world

## 📁 Project Structure

```
Universal Open Science Toolbox/
├── BULLETPROOF_PIPELINE.py              # Main framework
├── download_public_data.py               # Data downloader
├── test_suite/
│   └── universal_test_functions.py       # Test functions
├── examples/
│   └── basic_example.py                 # Working example
├── tests/                               # Test suite
├── rife_legacy/                         # Historical RIFE content
├── README.md                            # This file
├── GETTING_STARTED.md                   # Installation guide
├── API_REFERENCE.md                     # Technical documentation
├── EXAMPLES_GALLERY.md                  # Usage examples
├── CONTRIBUTING_GUIDE.md                # Development guidelines
├── requirements_universal.txt            # Dependencies
└── [test data files...]                 # Sample data
```

## 🔗 Related Projects

This toolbox was inspired by and built upon:
- **RIFE 28.0**: The theory that died but left behind bulletproof testing infrastructure (see `rife_legacy/`)
- **Open Science Movement**: Principles of transparency and reproducibility
- **Scientific Computing Community**: Tools and best practices

## 📖 Historical Context

The original RIFE implementation and documentation is preserved in the `rife_legacy/` folder for:
- **Historical record** of the theory that died
- **Educational value** in understanding scientific rigor
- **Research value** in studying failed theories
- **Inspiration** for future open science efforts

## 🧪 Test Battery

The project includes a comprehensive test battery to ensure reliability:

```bash
# Run all tests
python run_test_battery.py

# Run specific test suites
pytest tests/ -v

# View test results
cat test_battery_report.json
```

## 📚 Documentation

For detailed information, see:
- **`GETTING_STARTED.md`**: Installation and quick start guide
- **`API_REFERENCE.md`**: Complete API documentation
- **`EXAMPLES_GALLERY.md`**: Real-world usage examples
- **`CONTRIBUTING_GUIDE.md`**: Development and contribution guidelines

---

**RIFE is dead. Long live open science.**

*"This framework was forged in the fire of RIFE—a theory we put to the sword on real data, no excuses, and left for the world to audit. The code survived, even when the theory died. Now, anyone can plug in any new hypothesis, any field, and run the same bulletproof, tamper-proof, open science test—at home, for free, with receipts."* 