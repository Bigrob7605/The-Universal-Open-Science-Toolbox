#!/usr/bin/env python3
"""
Basic Example: Universal Open Science Toolbox
============================================

This example demonstrates how to use the Universal Open Science Toolbox
with the existing test data from RIFE.

Author: Universal Open Science Toolbox
License: MIT
Version: 1.0 - Basic Example
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from BULLETPROOF_PIPELINE import BulletproofPipeline
from test_suite.universal_test_functions import (
    basic_statistical_analysis,
    correlation_analysis,
    signal_detection_test,
    periodicity_test,
    clustering_analysis,
    dimensionality_analysis
)

def main():
    """Run a basic example with the existing test data"""
    
    print("🧬 Universal Open Science Toolbox - Basic Example")
    print("=" * 50)
    
    # Initialize pipeline
    pipeline = BulletproofPipeline({
        "example_name": "basic_demo",
        "description": "Basic demonstration of the toolbox"
    })
    
    # Load existing test data (iris dataset)
    print("\n📊 Loading test data...")
    if pipeline.load_data("test_data_iris.csv", "csv"):
        print("✅ Data loaded successfully")
        print(f"   Shape: {pipeline.data.shape}")
        print(f"   Data type: {pipeline.data.dtype}")
    else:
        print("❌ Failed to load data")
        return
    
    # Register test functions
    print("\n🔧 Registering test functions...")
    pipeline.register_test_function("statistical_analysis", basic_statistical_analysis)
    pipeline.register_test_function("correlation_analysis", correlation_analysis)
    pipeline.register_test_function("signal_detection", signal_detection_test)
    pipeline.register_test_function("periodicity_test", periodicity_test)
    pipeline.register_test_function("clustering_analysis", clustering_analysis)
    pipeline.register_test_function("dimensionality_analysis", dimensionality_analysis)
    
    print("✅ Registered 6 test functions")
    
    # Run individual tests
    print("\n🧪 Running individual tests...")
    
    # 1. Basic statistical analysis
    print("\n1. Basic Statistical Analysis")
    result = pipeline.run_test("statistical_analysis")
    if "error" not in result:
        truth_table = result["truth_table"]
        print(f"   Summary: {truth_table['summary']}")
        print(f"   Execution time: {result['execution_time']:.3f}s")
    else:
        print(f"   Error: {result['error']}")
    
    # 2. Correlation analysis
    print("\n2. Correlation Analysis")
    result = pipeline.run_test("correlation_analysis")
    if "error" not in result:
        truth_table = result["truth_table"]
        print(f"   Summary: {truth_table['summary']}")
        print(f"   Execution time: {result['execution_time']:.3f}s")
    else:
        print(f"   Error: {result['error']}")
    
    # 3. Signal detection test
    print("\n3. Signal Detection Test")
    result = pipeline.run_test("signal_detection", threshold=2.0)
    if "error" not in result:
        truth_table = result["truth_table"]
        print(f"   Summary: {truth_table['summary']}")
        print(f"   Execution time: {result['execution_time']:.3f}s")
    else:
        print(f"   Error: {result['error']}")
    
    # 4. Periodicity test
    print("\n4. Periodicity Test")
    result = pipeline.run_test("periodicity_test")
    if "error" not in result:
        truth_table = result["truth_table"]
        print(f"   Summary: {truth_table['summary']}")
        print(f"   Execution time: {result['execution_time']:.3f}s")
    else:
        print(f"   Error: {result['error']}")
    
    # 5. Clustering analysis
    print("\n5. Clustering Analysis")
    result = pipeline.run_test("clustering_analysis", max_clusters=4)
    if "error" not in result:
        truth_table = result["truth_table"]
        print(f"   Summary: {truth_table['summary']}")
        print(f"   Execution time: {result['execution_time']:.3f}s")
    else:
        print(f"   Error: {result['error']}")
    
    # 6. Dimensionality analysis
    print("\n6. Dimensionality Analysis")
    result = pipeline.run_test("dimensionality_analysis")
    if "error" not in result:
        truth_table = result["truth_table"]
        print(f"   Summary: {truth_table['summary']}")
        print(f"   Execution time: {result['execution_time']:.3f}s")
    else:
        print(f"   Error: {result['error']}")
    
    # Run batch test
    print("\n🚀 Running batch test...")
    batch_result = pipeline.run_batch_tests()
    
    if "overall_truth_table" in batch_result:
        overall = batch_result["overall_truth_table"]
        print(f"   Tests run: {len(overall['tests_run'])}")
        print(f"   Overall pass rate: {overall['overall_pass_rate']:.1%}")
    
    # Save results
    print("\n💾 Saving results...")
    results_file = pipeline.save_results("example_results.json")
    report_file = pipeline.generate_report("example_report.md")
    
    print(f"   Results saved to: {results_file}")
    print(f"   Report generated: {report_file}")
    
    # Display summary
    print("\n📊 Summary")
    print("=" * 30)
    print(f"Total tests run: {len(pipeline.test_results)}")
    
    successful_tests = sum(1 for result in pipeline.test_results.values() 
                          if "error" not in result)
    failed_tests = len(pipeline.test_results) - successful_tests
    
    print(f"Successful tests: {successful_tests}")
    print(f"Failed tests: {failed_tests}")
    
    if "overall_truth_table" in batch_result:
        overall = batch_result["overall_truth_table"]
        print(f"Overall pass rate: {overall['overall_pass_rate']:.1%}")
    
    print("\n✅ Example completed successfully!")
    print("\n📖 Check the generated files:")
    print(f"   - {results_file} (detailed results)")
    print(f"   - {report_file} (human-readable report)")

if __name__ == "__main__":
    main() 