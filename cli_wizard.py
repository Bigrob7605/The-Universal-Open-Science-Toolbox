#!/usr/bin/env python3
"""
CLI Wizard for Universal Open Science Toolbox
Interactive command-line interface for non-coders and coders alike.
"""

import argparse
import sys
import os
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
import numpy as np
import pandas as pd

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from BULLETPROOF_PIPELINE import BulletproofPipeline
from test_suite.universal_test_functions import get_available_tests
from download_public_data import PublicDataDownloader

class UniversalScienceWizard:
    """Interactive CLI wizard for the Universal Open Science Toolbox."""
    
    def __init__(self):
        self.pipeline = BulletproofPipeline()
        self.downloader = PublicDataDownloader()
        self.available_tests = get_available_tests()
        
    def print_banner(self):
        """Print the wizard banner."""
        print("\n" + "="*60)
        print("Universal Open Science Toolbox - CLI Wizard")
        print("="*60)
        print("Born from the fire of RIFE—where we proved open science works.")
        print("Now anyone can test any hypothesis, any field, any time.")
        print("="*60 + "\n")
    
    def interactive_mode(self):
        """Run the wizard in interactive mode."""
        self.print_banner()
        
        print("Welcome! Let's run a bulletproof scientific test together.")
        print("I'll guide you through each step.\n")
        
        # Step 1: Data selection
        data_path = self.select_data()
        if not data_path:
            print("ERROR: No data selected. Exiting.")
            return
        
        # Step 2: Test selection
        test_name = self.select_test()
        if not test_name:
            print("ERROR: No test selected. Exiting.")
            return
        
        # Step 3: Run test
        print(f"\n🚀 Running {test_name} on your data...")
        result = self.run_test(data_path, test_name)
        
        # Step 4: Show results
        self.show_results(result)
        
        # Step 5: Save results
        self.save_results(result)
        
        print("\nYour bulletproof scientific test is complete!")
        print("Check the generated files for your results.")
    
    def select_data(self) -> Optional[str]:
        """Interactive data selection."""
        print("STEP 1: Select Your Data")
        print("-" * 40)
        
        while True:
            print("\nOptions:")
            print("1. Use existing data file")
            print("2. Download sample dataset")
            print("3. List available datasets")
            print("4. Exit")
            
            choice = input("\nEnter your choice (1-4): ").strip()
            
            if choice == "1":
                return self.select_existing_file()
            elif choice == "2":
                return self.download_sample_data()
            elif choice == "3":
                self.list_available_datasets()
            elif choice == "4":
                return None
            else:
                print("ERROR: Invalid choice. Please try again.")
    
    def select_existing_file(self) -> Optional[str]:
        """Select an existing data file."""
        print("\nEnter the path to your data file:")
        print("(Supported formats: .csv, .h5, .fits, .npy)")
        
        file_path = input("File path: ").strip()
        
        if not file_path:
            return None
        
        if not os.path.exists(file_path):
            print(f"ERROR: File not found: {file_path}")
            return None
        
        print(f"File found: {file_path}")
        return file_path
    
    def download_sample_data(self) -> Optional[str]:
        """Download sample dataset."""
        print("\nAvailable sample datasets:")
        datasets = {
            "1": ("iris", "Iris flower dataset (classification)"),
            "2": ("titanic", "Titanic passenger data (survival analysis)"),
            "3": ("wine", "Wine quality dataset (regression)")
        }
        
        for key, (name, desc) in datasets.items():
            print(f"{key}. {name} - {desc}")
        
        choice = input("\nSelect dataset (1-3): ").strip()
        
        if choice in datasets:
            dataset_name = datasets[choice][0]
            print(f"\nDownloading {dataset_name} dataset...")
            
            try:
                result = self.downloader.download_dataset(dataset_name)
                if result['success']:
                    print(f"Downloaded: {result['file_path']}")
                    return result['file_path']
                else:
                    print(f"ERROR: Download failed: {result.get('error', 'Unknown error')}")
                    return None
            except Exception as e:
                print(f"ERROR: Download error: {e}")
                return None
        else:
            print("ERROR: Invalid choice.")
            return None
    
    def list_available_datasets(self):
        """List all available datasets."""
        print("\nAvailable Datasets:")
        print("-" * 40)
        
        try:
            info = self.downloader.list_available_datasets()
            for name, details in info['datasets'].items():
                print(f"• {name}: {details['description']}")
        except Exception as e:
            print(f"ERROR: Error listing datasets: {e}")
    
    def select_test(self) -> Optional[str]:
        """Interactive test selection."""
        print("\nSTEP 2: Select Your Test")
        print("-" * 40)
        
        print("\nAvailable tests:")
        for i, (test_name, description) in enumerate(self.available_tests.items(), 1):
            print(f"{i}. {test_name}")
            print(f"   {description}")
            print()
        
        while True:
            try:
                choice = input(f"Select test (1-{len(self.available_tests)}): ").strip()
                choice_num = int(choice)
                
                if 1 <= choice_num <= len(self.available_tests):
                    test_names = list(self.available_tests.keys())
                    selected_test = test_names[choice_num - 1]
                    print(f"Selected: {selected_test}")
                    return selected_test
                else:
                    print("ERROR: Invalid choice. Please try again.")
            except ValueError:
                print("ERROR: Please enter a number.")
    
    def run_test(self, data_path: str, test_name: str) -> Dict[str, Any]:
        """Run the selected test on the data."""
        try:
            # Load data
            print(f"📂 Loading data from: {data_path}")
            success = self.pipeline.load_data(data_path, "auto")
            
            if not success:
                return {"error": "Failed to load data"}
            
            # Register test if not already registered
            if test_name not in self.pipeline.test_functions:
                from test_suite.universal_test_functions import AVAILABLE_TESTS
                if test_name in AVAILABLE_TESTS:
                    self.pipeline.register_test_function(test_name, AVAILABLE_TESTS[test_name])
            
            # Run test
            print(f"Running {test_name}...")
            result = self.pipeline.run_test(test_name)
            
            return result
            
        except Exception as e:
            return {"error": f"Test execution failed: {str(e)}"}
    
    def show_results(self, result: Dict[str, Any]):
        """Display test results in a user-friendly format."""
        print("\nSTEP 3: Your Results")
        print("-" * 40)
        
        if "error" in result:
            print(f"ERROR: {result['error']}")
            return
        
        # Extract pass/fail information
        pass_fail = result.get("pass_fail", {})
        if pass_fail:
            print("\nPass/Fail Summary:")
            for criterion, passed in pass_fail.items():
                status = "PASS" if passed else "FAIL"
                print(f"  {criterion}: {status}")
        
        # Show key metrics
        metrics = result.get("metrics", {})
        if metrics:
            print("\nKey Metrics:")
            for key, value in metrics.items():
                if isinstance(value, (int, float)):
                    print(f"  {key}: {value:.4f}")
                else:
                    print(f"  {key}: {value}")
        
        # Show summary
        summary = result.get("summary", "")
        if summary:
            print(f"\nSummary: {summary}")
    
    def save_results(self, result: Dict[str, Any]):
        """Save results to files."""
        print("\nSTEP 4: Saving Results")
        print("-" * 40)
        
        try:
            # Save JSON results
            results_file = self.pipeline.save_results()
            print(f"Results saved to: {results_file}")
            
            # Generate report
            report_file = self.pipeline.generate_report()
            print(f"Report generated: {report_file}")
            
        except Exception as e:
            print(f"ERROR: Error saving results: {e}")
    
    def command_line_mode(self, args):
        """Run the wizard in command-line mode."""
        if args.list_tests:
            self.list_tests()
        elif args.list_datasets:
            self.list_available_datasets()
        elif args.run_test:
            self.run_command_line_test(args)
    
    def list_tests(self):
        """List all available tests."""
        print("\nAvailable Tests:")
        print("-" * 40)
        
        for test_name, description in self.available_tests.items():
            print(f"* {test_name}")
            print(f"  {description}")
            print()
    
    def run_command_line_test(self, args):
        """Run a test from command line arguments."""
        data_path = args.input
        test_name = args.test
        
        if not os.path.exists(data_path):
            print(f"ERROR: Data file not found: {data_path}")
            return
        
        print(f"Running {test_name} on {data_path}...")
        result = self.run_test(data_path, test_name)
        
        if "error" in result:
            print(f"ERROR: {result['error']}")
        else:
            print("Test completed successfully!")
            
            # Save results if requested
            if args.save:
                try:
                    results_file = self.pipeline.save_results(args.save)
                    report_file = self.pipeline.generate_report(f"{args.save}.md")
                    print(f"Results saved to: {results_file}")
                    print(f"Report saved to: {report_file}")
                except Exception as e:
                    print(f"ERROR: Error saving results: {e}")

def main():
    """Main entry point for the CLI wizard."""
    parser = argparse.ArgumentParser(
        description="Universal Open Science Toolbox - CLI Wizard",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode
  python cli_wizard.py
  
  # List available tests
  python cli_wizard.py --list-tests
  
  # List available datasets
  python cli_wizard.py --list-datasets
  
  # Run specific test
  python cli_wizard.py --input data.csv --test basic_statistical_analysis
  
  # Run test and save results
  python cli_wizard.py --input data.csv --test correlation_analysis --save my_results
        """
    )
    
    parser.add_argument("--input", "-i", help="Input data file path")
    parser.add_argument("--test", "-t", help="Test function name")
    parser.add_argument("--save", "-s", help="Save results with this prefix")
    parser.add_argument("--list-tests", action="store_true", help="List available tests")
    parser.add_argument("--list-datasets", action="store_true", help="List available datasets")
    parser.add_argument("--interactive", "-I", action="store_true", help="Run in interactive mode")
    
    args = parser.parse_args()
    
    wizard = UniversalScienceWizard()
    
    # Check if any command-line arguments were provided
    if any([args.input, args.test, args.save, args.list_tests, args.list_datasets]):
        wizard.command_line_mode(args)
    else:
        # Default to interactive mode
        wizard.interactive_mode()

if __name__ == "__main__":
    main() 