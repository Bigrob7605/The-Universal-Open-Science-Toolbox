#!/usr/bin/env python3
"""
Universal Public Data Download and Manifest Tool
==============================================

Download, hash, and manifest public datasets for reproducible science.
Handles "404 fallback" gracefully so framework doesn't die when files are missing.

Author: Universal Open Science Toolbox
License: MIT
Version: 1.0 - Universal Data Fetcher
"""

import requests
import hashlib
import json
import os
import time
import tempfile
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import argparse

# ======================================================================
# 1. PUBLIC DATASET DEFINITIONS
# ======================================================================

PUBLIC_DATASETS = {
    # Astronomy & Astrophysics
    "iris": {
        "url": "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv",
        "description": "Iris flower dataset (Fisher, 1936)",
        "format": "csv",
        "size_estimate": "4KB"
    },
    "titanic": {
        "url": "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv",
        "description": "Titanic passenger survival dataset",
        "format": "csv", 
        "size_estimate": "60KB"
    },
    "wine": {
        "url": "https://archive.ics.uci.edu/ml/machine-learning-databases/wine/wine.data",
        "description": "Wine quality dataset (UCI)",
        "format": "csv",
        "size_estimate": "11KB"
    },
    "diabetes": {
        "url": "https://raw.githubusercontent.com/scikit-learn/scikit-learn/main/sklearn/datasets/data/diabetes_data.csv.gz",
        "description": "Diabetes dataset (sklearn)",
        "format": "csv",
        "size_estimate": "15KB"
    },
    "breast_cancer": {
        "url": "https://raw.githubusercontent.com/scikit-learn/scikit-learn/main/sklearn/datasets/data/breast_cancer.csv",
        "description": "Breast cancer Wisconsin dataset",
        "format": "csv",
        "size_estimate": "30KB"
    },
    
    # Physics & Engineering
    "ligo_sample": {
        "url": "https://www.gw-openscience.org/eventapi/json/GWTC-1-confident/GW150914/v3/",
        "description": "LIGO GW150914 event data (JSON)",
        "format": "json",
        "size_estimate": "50KB"
    },
    "cern_opendata": {
        "url": "http://opendata.cern.ch/record/12361/files/demo.root",
        "description": "CERN Open Data sample (ROOT)",
        "format": "root",
        "size_estimate": "1MB"
    },
    
    # Climate & Environmental
    "noaa_temperature": {
        "url": "https://www.ncei.noaa.gov/data/global-summary-of-the-day/access/2024/",
        "description": "NOAA Global Summary of the Day",
        "format": "csv",
        "size_estimate": "100MB"
    },
    
    # Social Sciences
    "gapminder": {
        "url": "https://raw.githubusercontent.com/jennybc/gapminder/main/data-raw/08_gap-every-five-years.tsv",
        "description": "Gapminder life expectancy data",
        "format": "tsv",
        "size_estimate": "2KB"
    }
}

# ======================================================================
# 2. DATA DOWNLOAD AND MANIFEST CLASS
# ======================================================================

class PublicDataDownloader:
    """
    Universal public data downloader with bulletproof error handling
    and comprehensive manifest generation.
    """
    
    def __init__(self, output_dir: str = "data", timeout: int = 30):
        """
        Initialize the data downloader.
        
        Parameters:
        -----------
        output_dir : str
            Directory to save downloaded data
        timeout : int
            Request timeout in seconds
        """
        self.output_dir = Path(output_dir)
        self.timeout = timeout
        self.manifest = {}
        self.download_history = []
        
        # Create output directory
        self.output_dir.mkdir(exist_ok=True)
        
        print(f"Data will be saved to: {self.output_dir.absolute()}")
    
    def download_dataset(self, dataset_name: str, force_redownload: bool = False) -> Dict[str, any]:
        """
        Download a specific dataset with comprehensive error handling.
        
        Parameters:
        -----------
        dataset_name : str
            Name of the dataset to download
        force_redownload : bool
            Force re-download even if file exists
            
        Returns:
        --------
        dict : Download result with manifest information
        """
        if dataset_name not in PUBLIC_DATASETS:
            return {
                "success": False,
                "error": f"Dataset '{dataset_name}' not found",
                "available_datasets": list(PUBLIC_DATASETS.keys())
            }
        
        dataset_info = PUBLIC_DATASETS[dataset_name]
        output_file = self.output_dir / f"{dataset_name}.{dataset_info['format']}"
        
        # Check if file already exists
        if output_file.exists() and not force_redownload:
            print(f"Dataset '{dataset_name}' already exists: {output_file}")
            return self._generate_manifest(dataset_name, output_file, dataset_info)
        
        print(f"Downloading {dataset_name}...")
        print(f"   URL: {dataset_info['url']}")
        print(f"   Description: {dataset_info['description']}")
        
        try:
            # Download with timeout and error handling
            response = requests.get(
                dataset_info['url'], 
                timeout=self.timeout,
                headers={'User-Agent': 'Universal-Open-Science-Toolbox/1.0'}
            )
            response.raise_for_status()
            
            # Save file
            with open(output_file, 'wb') as f:
                f.write(response.content)
            
            # Generate manifest
            manifest = self._generate_manifest(dataset_name, output_file, dataset_info)
            
            # Log download
            self.download_history.append({
                "timestamp": datetime.now().isoformat(),
                "dataset": dataset_name,
                "url": dataset_info['url'],
                "file_size": len(response.content),
                "status": "success"
            })
            
            print(f"Downloaded {dataset_name}: {len(response.content)} bytes")
            return manifest
            
        except requests.exceptions.Timeout:
            error_msg = f"Timeout downloading {dataset_name} (>{self.timeout}s)"
            print(f"ERROR: {error_msg}")
            return {"success": False, "error": error_msg}
            
        except requests.exceptions.HTTPError as e:
            error_msg = f"HTTP error downloading {dataset_name}: {e}"
            print(f"ERROR: {error_msg}")
            return {"success": False, "error": error_msg}
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Network error downloading {dataset_name}: {e}"
            print(f"ERROR: {error_msg}")
            return {"success": False, "error": error_msg}
            
        except Exception as e:
            error_msg = f"Unexpected error downloading {dataset_name}: {e}"
            print(f"ERROR: {error_msg}")
            return {"success": False, "error": error_msg}
    
    def _generate_manifest(self, dataset_name: str, file_path: Path, dataset_info: Dict) -> Dict[str, any]:
        """Generate comprehensive manifest for downloaded dataset"""
        try:
            # Calculate file hash
            with open(file_path, 'rb') as f:
                file_hash = hashlib.sha256(f.read()).hexdigest()
            
            # Get file stats
            stat = file_path.stat()
            
            manifest = {
                "success": True,
                "dataset_name": dataset_name,
                "file_path": str(file_path.absolute()),
                "url": dataset_info['url'],
                "description": dataset_info['description'],
                "format": dataset_info['format'],
                "download_time": datetime.now().isoformat(),
                "file_size": stat.st_size,
                "file_hash": file_hash,
                "file_modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "metadata": {
                    "format": dataset_info['format'],
                    "size_estimate": dataset_info['size_estimate'],
                    "downloaded_by": "Universal Open Science Toolbox",
                    "version": "1.0"
                }
            }
            
            self.manifest[dataset_name] = manifest
            return manifest
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to generate manifest: {e}",
                "dataset_name": dataset_name
            }
    
    def download_multiple_datasets(self, dataset_names: List[str], 
                                 force_redownload: bool = False) -> Dict[str, any]:
        """
        Download multiple datasets with batch processing.
        
        Parameters:
        -----------
        dataset_names : list
            List of dataset names to download
        force_redownload : bool
            Force re-download even if files exist
            
        Returns:
        --------
        dict : Batch download results
        """
        print(f"🚀 Starting batch download of {len(dataset_names)} datasets...")
        
        results = {}
        successful = 0
        failed = 0
        
        for dataset_name in dataset_names:
            result = self.download_dataset(dataset_name, force_redownload)
            results[dataset_name] = result
            
            if result.get("success", False):
                successful += 1
            else:
                failed += 1
        
        batch_result = {
            "total_datasets": len(dataset_names),
            "successful": successful,
            "failed": failed,
            "results": results,
            "timestamp": datetime.now().isoformat()
        }
        
        print(f"📊 Batch download complete: {successful} successful, {failed} failed")
        return batch_result
    
    def download_all_datasets(self, force_redownload: bool = False) -> Dict[str, any]:
        """Download all available datasets"""
        return self.download_multiple_datasets(
            list(PUBLIC_DATASETS.keys()), 
            force_redownload
        )
    
    def save_manifest(self, output_path: str = None) -> str:
        """
        Save the complete manifest to a JSON file.
        
        Parameters:
        -----------
        output_path : str
            Path for manifest file (auto-generated if None)
            
        Returns:
        --------
        str : Path to saved manifest file
        """
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"data_manifest_{timestamp}.json"
        
        manifest_data = {
            "manifest_generated": datetime.now().isoformat(),
            "total_datasets": len(self.manifest),
            "download_history": self.download_history,
            "datasets": self.manifest
        }
        
        with open(output_path, 'w') as f:
            json.dump(manifest_data, f, indent=2, default=str)
        
        print(f"📋 Manifest saved to: {output_path}")
        return output_path
    
    def list_available_datasets(self) -> Dict[str, any]:
        """List all available datasets with information"""
        return {
            "total_available": len(PUBLIC_DATASETS),
            "datasets": PUBLIC_DATASETS,
            "categories": {
                "astronomy": ["iris", "titanic", "wine"],
                "physics": ["ligo_sample", "cern_opendata"],
                "climate": ["noaa_temperature"],
                "social_sciences": ["gapminder"]
            }
        }
    
    def verify_download(self, dataset_name: str) -> Dict[str, any]:
        """
        Verify a downloaded dataset by checking file integrity.
        
        Parameters:
        -----------
        dataset_name : str
            Name of the dataset to verify
            
        Returns:
        --------
        dict : Verification result
        """
        if dataset_name not in self.manifest:
            return {
                "success": False,
                "error": f"Dataset '{dataset_name}' not in manifest"
            }
        
        manifest = self.manifest[dataset_name]
        file_path = Path(manifest['file_path'])
        
        if not file_path.exists():
            return {
                "success": False,
                "error": f"File not found: {file_path}"
            }
        
        try:
            # Recalculate hash
            with open(file_path, 'rb') as f:
                current_hash = hashlib.sha256(f.read()).hexdigest()
            
            # Compare with stored hash
            hash_match = current_hash == manifest['file_hash']
            
            return {
                "success": True,
                "file_exists": True,
                "hash_match": hash_match,
                "stored_hash": manifest['file_hash'],
                "current_hash": current_hash,
                "file_size": file_path.stat().st_size
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Verification failed: {e}"
            }

# ======================================================================
# 3. COMMAND LINE INTERFACE
# ======================================================================

def main():
    """Main command-line interface for data downloader"""
    parser = argparse.ArgumentParser(
        description="Universal Public Data Download and Manifest Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Download a specific dataset
  python download_public_data.py --dataset=iris
  
  # Download multiple datasets
  python download_public_data.py --dataset=iris --dataset=titanic --dataset=wine
  
  # Download all available datasets
  python download_public_data.py --all
  
  # List available datasets
  python download_public_data.py --list
  
  # Verify downloaded dataset
  python download_public_data.py --verify=iris
        """
    )
    
    parser.add_argument("--dataset", "-d", action="append",
                       help="Dataset name to download (can specify multiple)")
    parser.add_argument("--all", "-a", action="store_true",
                       help="Download all available datasets")
    parser.add_argument("--list", "-l", action="store_true",
                       help="List all available datasets")
    parser.add_argument("--verify", "-v",
                       help="Verify a downloaded dataset")
    parser.add_argument("--output-dir", "-o", default="data",
                       help="Output directory for downloads")
    parser.add_argument("--force", "-f", action="store_true",
                       help="Force re-download even if file exists")
    parser.add_argument("--manifest", "-m",
                       help="Save manifest to specified file")
    parser.add_argument("--timeout", "-t", type=int, default=30,
                       help="Download timeout in seconds")
    
    args = parser.parse_args()
    
    # Initialize downloader
    downloader = PublicDataDownloader(args.output_dir, args.timeout)
    
    if args.list:
        # List available datasets
        info = downloader.list_available_datasets()
        print(f"Available datasets ({info['total_available']}):\n")
        
        for name, details in info['datasets'].items():
            print(f"  {name}:")
            print(f"    Description: {details['description']}")
            print(f"    Format: {details['format']}")
            print(f"    Size: {details['size_estimate']}")
            print(f"    URL: {details['url']}")
            print()
        
        print("Categories:")
        for category, datasets in info['categories'].items():
            print(f"  {category}: {', '.join(datasets)}")
        
        return
    
    if args.verify:
        # Verify a dataset
        result = downloader.verify_download(args.verify)
        if result['success']:
            print(f"Dataset '{args.verify}' verification:")
            print(f"   File exists: {result['file_exists']}")
            print(f"   Hash match: {result['hash_match']}")
            print(f"   File size: {result['file_size']} bytes")
        else:
            print(f"ERROR: Verification failed: {result['error']}")
        return
    
    # Determine datasets to download
    if args.all:
        datasets_to_download = list(PUBLIC_DATASETS.keys())
    elif args.dataset:
        datasets_to_download = args.dataset
    else:
        print("ERROR: No datasets specified. Use --dataset, --all, --list, or --verify")
        return
    
    # Download datasets
    if len(datasets_to_download) == 1:
        result = downloader.download_dataset(datasets_to_download[0], args.force)
        if result['success']:
            print(f"Successfully downloaded {datasets_to_download[0]}")
        else:
            print(f"ERROR: Failed to download {datasets_to_download[0]}: {result['error']}")
    else:
        result = downloader.download_multiple_datasets(datasets_to_download, args.force)
        print(f"Batch download complete: {result['successful']} successful, {result['failed']} failed")
    
    # Save manifest
    manifest_file = downloader.save_manifest(args.manifest)
    print(f"Manifest saved to: {manifest_file}")

if __name__ == "__main__":
    main() 