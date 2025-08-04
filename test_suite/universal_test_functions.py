#!/usr/bin/env python3
"""
Universal Test Functions for Open Science
========================================

Plug-and-play test functions for the bulletproof pipeline.
Drop in any new theory/model as a function/class and the pipeline 
tests its predictions against the data.

Author: Universal Open Science Toolbox
License: MIT
Version: 1.0 - Universal Test Functions
"""

import numpy as np
import pandas as pd
from scipy import stats
from scipy.signal import find_peaks
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA
from typing import Dict, Any, List, Optional
import warnings
import json
from datetime import datetime

# Global configuration
DEFAULT_THRESHOLDS = {
    "statistical_significance": 0.05,
    "correlation_threshold": 0.7,
    "snr_threshold": 5.0,
    "outlier_threshold": 3.0,
    "clustering_silhouette": 0.5,
    "periodicity_significance": 0.01,
    "detection_confidence": 0.95
}

# Truth table schema for consistent results
TRUTH_SCHEMA = {
    "test_name": str,
    "timestamp": str,
    "pass_fail": dict,       # MUST contain bools
    "metrics": dict,
    "evidence": dict,        # raw arrays, plots links
    "falsification_notes": str
}

def ensure_json_serializable(obj):
    """
    Convert numpy types to JSON-serializable Python types.
    """
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.bool_):
        return bool(obj)
    elif isinstance(obj, dict):
        return {k: ensure_json_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [ensure_json_serializable(item) for item in obj]
    else:
        return obj

def create_truth_table(test_name: str, pass_fail: dict, metrics: dict, 
                      evidence: dict = None, falsification_notes: str = "") -> dict:
    """
    Create a standardized truth table with proper JSON serialization.
    """
    return ensure_json_serializable({
        "test_name": test_name,
        "timestamp": datetime.now().isoformat(),
        "pass_fail": pass_fail,
        "metrics": metrics,
        "evidence": evidence or {},
        "falsification_notes": falsification_notes
    })

def basic_statistical_analysis(data: np.ndarray, **kwargs) -> Dict[str, Any]:
    """
    Basic statistical analysis of any dataset.
    
    Parameters:
    -----------
    data : np.ndarray
        Input data array
    **kwargs : Additional parameters
        
    Returns:
    --------
    dict : Statistical analysis results with pass/fail criteria
    """
    try:
        # Ensure data is 2D
        if data.ndim == 1:
            data_2d = data.reshape(-1, 1)
        else:
            data_2d = data
        
        # Calculate basic statistics
        mean_values = np.mean(data_2d, axis=0)
        std_values = np.std(data_2d, axis=0)
        median_values = np.median(data_2d, axis=0)
        
        # Normality tests
        normality_tests = []
        for i in range(data_2d.shape[1]):
            try:
                stat, p_value = stats.normaltest(data_2d[:, i])
                normality_tests.append({
                    "column": i,
                    "statistic": stat,
                    "p_value": p_value,
                    "is_normal": p_value > DEFAULT_THRESHOLDS["statistical_significance"]
                })
            except:
                normality_tests.append({
                    "column": i,
                    "statistic": None,
                    "p_value": None,
                    "is_normal": None
                })
        
        # Outlier detection
        outlier_analysis = []
        for i in range(data_2d.shape[1]):
            z_scores = np.abs(stats.zscore(data_2d[:, i]))
            outliers = np.sum(z_scores > DEFAULT_THRESHOLDS["outlier_threshold"])
            outlier_analysis.append({
                "column": i,
                "outliers": int(outliers),
                "outlier_percentage": float(outliers / len(data_2d) * 100)
            })
        
        # Pass/fail criteria
        pass_fail = {
            "data_loaded": True,
            "has_sufficient_data": len(data_2d) > 10,
            "no_extreme_outliers": all(oa["outlier_percentage"] < 10 for oa in outlier_analysis),
            "statistical_analysis_complete": True
        }
        
        # Create metrics
        metrics = {
            "mean": mean_values.tolist(),
            "std": std_values.tolist(),
            "median": median_values.tolist(),
            "shape": data_2d.shape,
            "normality_tests": normality_tests,
            "outlier_analysis": outlier_analysis
        }
        
        # Create evidence
        evidence = {
            "raw_data_shape": data_2d.shape,
            "data_summary": {
                "min": np.min(data_2d, axis=0).tolist(),
                "max": np.max(data_2d, axis=0).tolist(),
                "range": (np.max(data_2d, axis=0) - np.min(data_2d, axis=0)).tolist()
            }
        }
        
        return create_truth_table(
            test_name="basic_statistical_analysis",
            pass_fail=pass_fail,
            metrics=metrics,
            evidence=evidence
        )
        
    except Exception as e:
        return create_truth_table(
            test_name="basic_statistical_analysis",
            pass_fail={"data_loaded": False, "statistical_analysis_complete": False},
            metrics={"error": f"Statistical analysis failed: {str(e)}"},
            evidence={},
            falsification_notes=f"Analysis failed with error: {str(e)}"
        )

def correlation_analysis(data: np.ndarray, **kwargs) -> Dict[str, Any]:
    """
    Correlation analysis between variables in the dataset.
    
    Parameters:
    -----------
    data : np.ndarray
        Input data array
    **kwargs : Additional parameters
        
    Returns:
    --------
    dict : Correlation analysis results with pass/fail criteria
    """
    try:
        # Ensure data is 2D
        if data.ndim == 1:
            data_2d = data.reshape(-1, 1)
        else:
            data_2d = data
        
        # Check if we have enough columns for correlation
        if data_2d.shape[1] < 2:
            return create_truth_table(
                test_name="correlation_analysis",
                pass_fail={"correlation_analysis_complete": False, "data_suitable_for_correlation": False},
                metrics={"error": "Correlation analysis requires at least 2 variables"},
                evidence={"data_shape": data_2d.shape},
                falsification_notes="Data has insufficient variables for correlation analysis"
            )
        
        # Calculate correlation matrices
        pearson_corr = np.corrcoef(data_2d.T)
        
        # Handle spearman correlation - it returns a scalar for 2 variables
        if data_2d.shape[1] == 2:
            spearman_val = stats.spearmanr(data_2d[:, 0], data_2d[:, 1])[0]
            spearman_corr = np.array([[1.0, spearman_val], [spearman_val, 1.0]])
        else:
            spearman_corr = stats.spearmanr(data_2d)[0]
        
        # Find strong correlations
        strong_correlations = []
        threshold = kwargs.get('correlation_threshold', DEFAULT_THRESHOLDS["correlation_threshold"])
        
        for i in range(data_2d.shape[1]):
            for j in range(i+1, data_2d.shape[1]):
                pearson_val = pearson_corr[i, j]
                spearman_val = spearman_corr[i, j]
                
                if abs(pearson_val) > threshold or abs(spearman_val) > threshold:
                    strong_correlations.append({
                        "variables": f"{i}-{j}",
                        "pearson_correlation": float(pearson_val),
                        "spearman_correlation": float(spearman_val),
                        "is_strong": abs(pearson_val) > threshold or abs(spearman_val) > threshold
                    })
        
        # Pass/fail criteria
        pass_fail = {
            "correlation_analysis_complete": True,
            "has_strong_correlations": len(strong_correlations) > 0,
            "data_suitable_for_correlation": data_2d.shape[1] > 1
        }
        
        # Create metrics
        metrics = {
            "pearson_correlation": pearson_corr.tolist(),
            "spearman_correlation": spearman_corr.tolist(),
            "strong_correlations": strong_correlations,
            "correlation_threshold": threshold
        }
        
        # Create evidence
        evidence = {
            "data_shape": data_2d.shape,
            "correlation_matrix_shape": pearson_corr.shape
        }
        
        return create_truth_table(
            test_name="correlation_analysis",
            pass_fail=pass_fail,
            metrics=metrics,
            evidence=evidence
        )
        
    except Exception as e:
        return create_truth_table(
            test_name="correlation_analysis",
            pass_fail={"correlation_analysis_complete": False},
            metrics={"error": f"Correlation analysis failed: {str(e)}"},
            evidence={},
            falsification_notes=f"Analysis failed with error: {str(e)}"
        )

def signal_detection_test(data: np.ndarray, **kwargs) -> Dict[str, Any]:
    """
    Signal detection test for time series or signal data.
    
    Parameters:
    -----------
    data : np.ndarray
        Input data array (time series)
    threshold : float, optional
        Detection threshold (default: 3.0)
    window_size : int, optional
        Window size for analysis (default: 100)
        
    Returns:
    --------
    dict : Signal detection results with pass/fail criteria
    """
    try:
        # Ensure data is 1D for signal processing
        if data.ndim > 1:
            data_flat = data.flatten()
        else:
            data_flat = data
        
        threshold = kwargs.get('threshold', DEFAULT_THRESHOLDS["snr_threshold"])
        window_size = kwargs.get('window_size', 100)
        
        # Signal statistics
        signal_mean = np.mean(data_flat)
        signal_std = np.std(data_flat)
        snr = signal_mean / signal_std if signal_std > 0 else 0
        
        # Peak detection
        peaks, properties = find_peaks(data_flat, height=threshold)
        num_peaks = len(peaks)
        
        # Frequency analysis
        fft = np.fft.fft(data_flat)
        power_spectrum = np.abs(fft)**2
        dominant_freq_idx = np.argmax(power_spectrum[1:len(power_spectrum)//2]) + 1
        dominant_frequency = dominant_freq_idx / len(data_flat)
        dominant_power = power_spectrum[dominant_freq_idx]
        
        # Moving average
        moving_avg = np.convolve(data_flat, np.ones(window_size)/window_size, mode='valid')
        
        # Pass/fail criteria
        pass_fail = {
            "signal_detected": bool(num_peaks > 0),
            "snr_above_threshold": bool(snr > DEFAULT_THRESHOLDS["snr_threshold"]),
            "peaks_detected": bool(num_peaks > 0),
            "frequency_analysis_complete": True
        }
        
        # Create metrics
        metrics = {
            "signal_statistics": {
                "mean": float(signal_mean),
                "std": float(signal_std),
                "snr": float(snr),
                "snr_threshold": DEFAULT_THRESHOLDS["snr_threshold"]
            },
            "peak_detection": {
                "num_peaks": int(num_peaks),
                "peak_positions": peaks.tolist(),
                "detection_threshold": float(threshold)
            },
            "frequency_analysis": {
                "dominant_frequency": float(dominant_frequency),
                "dominant_power": float(dominant_power),
                "total_power": float(np.sum(power_spectrum))
            },
            "moving_average": {
                "window_size": int(window_size),
                "mean": float(np.mean(moving_avg)),
                "std": float(np.std(moving_avg))
            },
            "detection_summary": {
                "signal_detected": bool(num_peaks > 0),
                "peaks_detected": bool(num_peaks > 0),
                "signal_strength": "strong" if snr > 5 else "moderate" if snr > 2 else "weak"
            }
        }
        
        # Create evidence
        evidence = {
            "data_length": len(data_flat),
            "fft_length": len(fft),
            "moving_avg_length": len(moving_avg)
        }
        
        return create_truth_table(
            test_name="signal_detection_test",
            pass_fail=pass_fail,
            metrics=metrics,
            evidence=evidence
        )
        
    except Exception as e:
        return create_truth_table(
            test_name="signal_detection_test",
            pass_fail={"signal_detected": False, "frequency_analysis_complete": False},
            metrics={"error": f"Signal detection failed: {str(e)}"},
            evidence={},
            falsification_notes=f"Analysis failed with error: {str(e)}"
        )

def periodicity_test(data: np.ndarray, **kwargs) -> Dict[str, Any]:
    """
    Test for periodic patterns in the data.
    
    Parameters:
    -----------
    data : np.ndarray
        Input data array
    max_period : int, optional
        Maximum period to test (default: len(data)//4)
        
    Returns:
    --------
    dict : Periodicity test results with pass/fail criteria
    """
    try:
        # Ensure data is 1D
        if data.ndim > 1:
            data_flat = data.flatten()
        else:
            data_flat = data
        
        max_period = kwargs.get('max_period', len(data_flat)//4)
        
        # Autocorrelation analysis
        autocorr = np.correlate(data_flat, data_flat, mode='full')
        autocorr = autocorr[len(data_flat)-1:]
        
        # Find peaks in autocorrelation (periods)
        peaks, _ = find_peaks(autocorr[:max_period], height=np.max(autocorr)*0.5)
        
        detected_periods = []
        for peak in peaks:
            if peak > 1:  # Avoid lag 0
                correlation = autocorr[peak]
                significance = correlation / np.max(autocorr)
                detected_periods.append({
                    "lag": int(peak),
                    "correlation": float(correlation),
                    "significance": float(significance)
                })
        
        # Sort by significance
        detected_periods.sort(key=lambda x: x["significance"], reverse=True)
        
        # Pass/fail criteria
        has_periodicity = len(detected_periods) > 0
        strongest_period = detected_periods[0]["lag"] if detected_periods else None
        periodicity_strength = "strong" if has_periodicity and detected_periods[0]["significance"] > 0.8 else "moderate" if has_periodicity else "none"
        
        pass_fail = {
            "has_periodicity": bool(has_periodicity),
            "periodicity_analysis_complete": True,
            "significant_periods_found": bool(len([p for p in detected_periods if p["significance"] > DEFAULT_THRESHOLDS["periodicity_significance"]]) > 0)
        }
        
        # Create metrics
        metrics = {
            "autocorrelation_analysis": {
                "detected_periods": detected_periods,
                "max_period_tested": int(max_period)
            },
            "periodicity_summary": {
                "has_periodicity": bool(has_periodicity),
                "strongest_period": strongest_period,
                "periodicity_strength": periodicity_strength,
                "num_periods_detected": len(detected_periods)
            }
        }
        
        # Create evidence
        evidence = {
            "data_length": len(data_flat),
            "autocorr_length": len(autocorr),
            "max_period_tested": max_period
        }
        
        return create_truth_table(
            test_name="periodicity_test",
            pass_fail=pass_fail,
            metrics=metrics,
            evidence=evidence
        )
        
    except Exception as e:
        return create_truth_table(
            test_name="periodicity_test",
            pass_fail={"has_periodicity": False, "periodicity_analysis_complete": False},
            metrics={"error": f"Periodicity test failed: {str(e)}"},
            evidence={},
            falsification_notes=f"Analysis failed with error: {str(e)}"
        )

def clustering_analysis(data: np.ndarray, **kwargs) -> Dict[str, Any]:
    """
    Basic clustering analysis using K-means.
    
    Parameters:
    -----------
    data : np.ndarray
        Input data array
    max_clusters : int, optional
        Maximum number of clusters to test (default: 5)
        
    Returns:
    --------
    dict : Clustering analysis results with pass/fail criteria
    """
    try:
        # Ensure data is 2D
        if data.ndim == 1:
            data_2d = data.reshape(-1, 1)
        else:
            data_2d = data
        
        max_clusters = kwargs.get('max_clusters', 5)
        max_clusters = min(max_clusters, len(data_2d) - 1)  # Can't have more clusters than samples
        
        # Test different numbers of clusters
        cluster_analysis = []
        silhouette_scores = []
        
        for k in range(2, max_clusters + 1):
            try:
                kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
                cluster_labels = kmeans.fit_predict(data_2d)
                
                # Calculate silhouette score
                silhouette = silhouette_score(data_2d, cluster_labels)
                silhouette_scores.append(silhouette)
                
                # Get cluster sizes
                unique, counts = np.unique(cluster_labels, return_counts=True)
                cluster_sizes = counts.tolist()
                
                cluster_analysis.append({
                    "n_clusters": k,
                    "inertia": float(kmeans.inertia_),
                    "silhouette_score": float(silhouette),
                    "cluster_sizes": cluster_sizes
                })
            except Exception as e:
                cluster_analysis.append({
                    "n_clusters": k,
                    "inertia": None,
                    "silhouette_score": None,
                    "cluster_sizes": None,
                    "error": str(e)
                })
        
        # Find optimal number of clusters
        valid_scores = [ca["silhouette_score"] for ca in cluster_analysis if ca["silhouette_score"] is not None]
        if valid_scores:
            optimal_clusters = cluster_analysis[np.argmax(valid_scores)]["n_clusters"]
            optimal_silhouette = max(valid_scores)
        else:
            optimal_clusters = 2
            optimal_silhouette = 0
        
        # Pass/fail criteria
        pass_fail = {
            "clustering_analysis_complete": True,
            "optimal_clusters_found": bool(optimal_silhouette > DEFAULT_THRESHOLDS["clustering_silhouette"]),
            "data_suitable_for_clustering": bool(len(data_2d) > 10)
        }
        
        # Create metrics
        metrics = {
            "cluster_analysis": cluster_analysis,
            "optimal_clusters": int(optimal_clusters),
            "optimal_silhouette": float(optimal_silhouette)
        }
        
        # Create evidence
        evidence = {
            "data_shape": data_2d.shape,
            "max_clusters_tested": max_clusters,
            "silhouette_scores": silhouette_scores
        }
        
        return create_truth_table(
            test_name="clustering_analysis",
            pass_fail=pass_fail,
            metrics=metrics,
            evidence=evidence
        )
        
    except Exception as e:
        return create_truth_table(
            test_name="clustering_analysis",
            pass_fail={"clustering_analysis_complete": False},
            metrics={"error": f"Clustering analysis failed: {str(e)}"},
            evidence={},
            falsification_notes=f"Analysis failed with error: {str(e)}"
        )

def dimensionality_analysis(data: np.ndarray, **kwargs) -> Dict[str, Any]:
    """
    Analyze the dimensionality and structure of the data.
    
    Parameters:
    -----------
    data : np.ndarray
        Input data array
    **kwargs : Additional parameters
        
    Returns:
    --------
    dict : Dimensionality analysis results with pass/fail criteria
    """
    try:
        # Ensure data is 2D
        if data.ndim == 1:
            data_2d = data.reshape(-1, 1)
        else:
            data_2d = data
        
        # Basic dimensionality info
        dimensions = {
            "samples": int(data_2d.shape[0]),
            "features": int(data_2d.shape[1]),
            "total_elements": int(data_2d.size)
        }
        
        # PCA analysis for dimensionality reduction
        if data_2d.shape[1] > 1:
            pca = PCA()
            pca.fit(data_2d)
            
            # Calculate explained variance
            explained_variance_ratio = pca.explained_variance_ratio_
            cumulative_variance = np.cumsum(explained_variance_ratio)
            
            # Find number of components for different variance thresholds
            dims_90 = np.argmax(cumulative_variance >= 0.9) + 1
            dims_95 = np.argmax(cumulative_variance >= 0.95) + 1
            dims_99 = np.argmax(cumulative_variance >= 0.99) + 1
            
            effective_dimensions = {
                "dimensions_for_90_percent_variance": int(dims_90),
                "dimensions_for_95_percent_variance": int(dims_95),
                "dimensions_for_99_percent_variance": int(dims_99),
                "dimensionality_reduction_potential": int(data_2d.shape[1] - dims_95)
            }
        else:
            effective_dimensions = {
                "dimensions_for_90_percent_variance": 1,
                "dimensions_for_95_percent_variance": 1,
                "dimensions_for_99_percent_variance": 1,
                "dimensionality_reduction_potential": 0
            }
        
        # Pass/fail criteria
        pass_fail = {
            "dimensionality_analysis_complete": True,
            "data_has_multiple_features": bool(data_2d.shape[1] > 1),
            "dimensionality_reduction_possible": bool(effective_dimensions["dimensionality_reduction_potential"] > 0)
        }
        
        # Create metrics
        metrics = {
            "dimensions": dimensions,
            "effective_dimensions": effective_dimensions
        }
        
        # Create evidence
        evidence = {
            "data_shape": data_2d.shape,
            "pca_components": data_2d.shape[1] if data_2d.shape[1] > 1 else 1
        }
        
        return create_truth_table(
            test_name="dimensionality_analysis",
            pass_fail=pass_fail,
            metrics=metrics,
            evidence=evidence
        )
        
    except Exception as e:
        return create_truth_table(
            test_name="dimensionality_analysis",
            pass_fail={"dimensionality_analysis_complete": False},
            metrics={"error": f"Dimensionality analysis failed: {str(e)}"},
            evidence={},
            falsification_notes=f"Analysis failed with error: {str(e)}"
        )

def custom_test_template(data: np.ndarray, **kwargs) -> Dict[str, Any]:
    """
    Template for custom test functions.
    
    Parameters:
    -----------
    data : np.ndarray
        Input data array
    **kwargs : Additional parameters
        
    Returns:
    --------
    dict : Custom test results with pass/fail criteria
    """
    try:
        # Your custom analysis here
        result = {
            "custom_metric": 42.0,
            "threshold": kwargs.get('threshold', 5.0),
            "analysis_complete": True
        }
        
        # Pass/fail criteria
        pass_fail = {
            "custom_test_passed": result["custom_metric"] > result["threshold"],
            "analysis_complete": True
        }
        
        result["pass_fail"] = pass_fail
        return result
        
    except Exception as e:
        return {
            "error": f"Custom test failed: {str(e)}",
            "pass_fail": {"custom_test_passed": False}
        }

# Import enzyme functions
try:
    from domain.bio import get_enzyme_functions
    ENZYME_FUNCTIONS = get_enzyme_functions()
except ImportError:
    ENZYME_FUNCTIONS = {}

# Import climate functions
try:
    from domain.climate import get_climate_functions
    CLIMATE_FUNCTIONS = get_climate_functions()
except ImportError:
    CLIMATE_FUNCTIONS = {}

# Import seismology functions
try:
    from domain.seismology import get_seismology_functions
    SEISMOLOGY_FUNCTIONS = get_seismology_functions()
except ImportError:
    SEISMOLOGY_FUNCTIONS = {}

# Available tests dictionary
AVAILABLE_TESTS = {
    "basic_statistical_analysis": basic_statistical_analysis,
    "correlation_analysis": correlation_analysis,
    "signal_detection_test": signal_detection_test,
    "periodicity_test": periodicity_test,
    "clustering_analysis": clustering_analysis,
    "dimensionality_analysis": dimensionality_analysis,
    "custom_test_template": custom_test_template,
    **ENZYME_FUNCTIONS,  # Add enzyme functions
    **CLIMATE_FUNCTIONS,  # Add climate functions
    **SEISMOLOGY_FUNCTIONS  # Add seismology functions
}

def get_available_tests() -> Dict[str, str]:
    """Get list of available test functions with descriptions."""
    base_tests = {
        "basic_statistical_analysis": "Basic statistical analysis (mean, std, normality, outliers)",
        "correlation_analysis": "Correlation analysis between variables",
        "signal_detection_test": "Signal detection in time series data",
        "periodicity_test": "Test for periodic patterns in data",
        "clustering_analysis": "K-means clustering with optimal k selection",
        "dimensionality_analysis": "Analyze data dimensionality and structure",
        "custom_test_template": "Template for custom test functions"
    }
    
    # Add enzyme test descriptions
    enzyme_descriptions = {
        "enzyme_sequence_analysis": "Analyze enzyme sequence properties and characteristics",
        "enzyme_structure_validation": "Validate enzyme structure properties from PDB file",
        "enzyme_mutation_analysis": "Analyze mutations between wild-type and mutant sequences",
        "enzyme_activity_prediction": "Predict enzyme activity based on sequence and structure"
    }
    
    # Add climate test descriptions
    climate_descriptions = {
        "climate_trend_analysis": "Analyze climate trends in temperature and CO2 data",
        "climate_change_detection": "Detect climate change signals using statistical tests",
        "seasonal_climate_analysis": "Analyze seasonal patterns in climate data"
    }
    
    # Add seismology test descriptions
    seismology_descriptions = {
        "heat_warning_correlation_index": "Calculate HWCI for heat effects",
        "stress_perturbation_analysis": "Analyze stress perturbation from heat sources",
        "seismic_modulator_analysis": "Analyze multiple seismic modulators (solar, climatic, heat)"
    }
    
    return {**base_tests, **enzyme_descriptions, **climate_descriptions, **seismology_descriptions}

def register_custom_test(test_name: str, test_function: callable) -> None:
    """Register a custom test function."""
    AVAILABLE_TESTS[test_name] = test_function 