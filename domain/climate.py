#!/usr/bin/env python3
"""
Climate Analysis Domain
Universal Open Science Toolbox

Real climate data analysis functions for temperature trends, CO2 levels,
sea level rise, and climate change detection.

Author: Universal Open Science Toolbox
License: MIT
Version: 1.0 - Climate Domain
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple
from scipy import stats
from scipy.signal import detrend
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller
import warnings
warnings.filterwarnings('ignore')

# Climate-specific thresholds
CLIMATE_THRESHOLDS = {
    "temperature_trend_significance": 0.05,
    "co2_trend_significance": 0.05,
    "warming_rate_threshold": 0.1,  # °C per decade
    "co2_increase_threshold": 2.0,  # ppm per year
    "seasonal_strength_threshold": 0.3,
    "trend_strength_threshold": 0.5
}

def ensure_json_serializable(obj):
    """Ensure object is JSON serializable."""
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.bool_):
        return bool(obj)
    elif isinstance(obj, dict):
        return {key: ensure_json_serializable(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [ensure_json_serializable(item) for item in obj]
    else:
        return obj

def create_truth_table(test_name: str, pass_fail: dict, metrics: dict, 
                      evidence: dict = None, falsification_notes: str = "") -> dict:
    """Create standardized truth table output."""
    return {
        "test_name": test_name,
        "pass_fail": ensure_json_serializable(pass_fail),
        "metrics": ensure_json_serializable(metrics),
        "evidence": ensure_json_serializable(evidence) if evidence else {},
        "falsification_notes": falsification_notes,
        "timestamp": pd.Timestamp.now().isoformat()
    }

def climate_trend_analysis(data: np.ndarray, **kwargs) -> Dict[str, Any]:
    """
    Analyze climate trends in temperature and CO2 data.
    
    Parameters:
    -----------
    data : np.ndarray
        Climate data array with columns [year, month, temp_anomaly, co2_ppm, ...]
    **kwargs : Additional parameters
        
    Returns:
    --------
    dict : Climate trend analysis results
    """
    try:
        # Convert to DataFrame if needed
        if isinstance(data, np.ndarray):
            if data.ndim == 1:
                # Single time series
                df = pd.DataFrame({
                    'value': data,
                    'time': np.arange(len(data))
                })
            else:
                # Multi-column data
                df = pd.DataFrame(data, columns=['year', 'month', 'temp_anomaly', 'co2_ppm', 
                                               'sea_level', 'arctic_ice', 'antarctic_ice'])
        else:
            df = data
        
        # Extract key variables
        if 'temp_anomaly' in df.columns:
            temp_data = df['temp_anomaly'].dropna()
            time_temp = np.arange(len(temp_data))
        else:
            temp_data = df.iloc[:, 2] if df.shape[1] > 2 else df.iloc[:, 0]
            time_temp = np.arange(len(temp_data))
        
        if 'co2_ppm' in df.columns:
            co2_data = df['co2_ppm'].dropna()
            time_co2 = np.arange(len(co2_data))
        else:
            co2_data = df.iloc[:, 3] if df.shape[1] > 3 else None
            time_co2 = np.arange(len(co2_data)) if co2_data is not None else None
        
        # Temperature trend analysis
        temp_trend = None
        temp_slope = None
        temp_r_squared = None
        temp_p_value = None
        
        if len(temp_data) > 10:
            temp_slope, temp_intercept, temp_r_value, temp_p_value, temp_std_err = stats.linregress(time_temp, temp_data)
            temp_r_squared = temp_r_value ** 2
            temp_trend = "warming" if temp_slope > 0 else "cooling"
        
        # CO2 trend analysis
        co2_trend = None
        co2_slope = None
        co2_r_squared = None
        co2_p_value = None
        
        if co2_data is not None and len(co2_data) > 10:
            co2_slope, co2_intercept, co2_r_value, co2_p_value, co2_std_err = stats.linregress(time_co2, co2_data)
            co2_r_squared = co2_r_value ** 2
            co2_trend = "increasing" if co2_slope > 0 else "decreasing"
        
        # Detrending analysis
        temp_detrended = None
        co2_detrended = None
        
        if temp_data is not None and len(temp_data) > 10:
            temp_detrended = detrend(temp_data)
        
        if co2_data is not None and len(co2_data) > 10:
            co2_detrended = detrend(co2_data)
        
        # Seasonal decomposition (if enough data)
        temp_seasonal = None
        co2_seasonal = None
        
        if len(temp_data) > 24:  # At least 2 years of monthly data
            try:
                temp_decomposition = seasonal_decompose(temp_data, period=12, extrapolate_trend='freq')
                temp_seasonal = temp_decomposition.seasonal
            except:
                temp_seasonal = None
        
        if co2_data is not None and len(co2_data) > 24:
            try:
                co2_decomposition = seasonal_decompose(co2_data, period=12, extrapolate_trend='freq')
                co2_seasonal = co2_decomposition.seasonal
            except:
                co2_seasonal = None
        
        # Pass/fail criteria
        pass_fail = {
            "temperature_trend_detected": bool(temp_trend is not None),
            "temperature_warming_significant": bool(temp_p_value is not None and temp_p_value < CLIMATE_THRESHOLDS["temperature_trend_significance"]),
            "co2_trend_detected": bool(co2_trend is not None),
            "co2_increase_significant": bool(co2_p_value is not None and co2_p_value < CLIMATE_THRESHOLDS["co2_trend_significance"]),
            "warming_rate_above_threshold": bool(temp_slope is not None and temp_slope > CLIMATE_THRESHOLDS["warming_rate_threshold"]),
            "co2_increase_above_threshold": bool(co2_slope is not None and co2_slope > CLIMATE_THRESHOLDS["co2_increase_threshold"]),
            "seasonal_patterns_detected": bool(temp_seasonal is not None or co2_seasonal is not None)
        }
        
        # Create metrics
        metrics = {
            "temperature_analysis": {
                "trend": temp_trend,
                "slope": float(temp_slope) if temp_slope is not None else None,
                "r_squared": float(temp_r_squared) if temp_r_squared is not None else None,
                "p_value": float(temp_p_value) if temp_p_value is not None else None,
                "mean": float(np.mean(temp_data)) if temp_data is not None else None,
                "std": float(np.std(temp_data)) if temp_data is not None else None
            },
            "co2_analysis": {
                "trend": co2_trend,
                "slope": float(co2_slope) if co2_slope is not None else None,
                "r_squared": float(co2_r_squared) if co2_r_squared is not None else None,
                "p_value": float(co2_p_value) if co2_p_value is not None else None,
                "mean": float(np.mean(co2_data)) if co2_data is not None else None,
                "std": float(np.std(co2_data)) if co2_data is not None else None
            },
            "detrending_analysis": {
                "temp_detrended_std": float(np.std(temp_detrended)) if temp_detrended is not None else None,
                "co2_detrended_std": float(np.std(co2_detrended)) if co2_detrended is not None else None
            },
            "seasonal_analysis": {
                "temp_seasonal_strength": float(np.std(temp_seasonal)) if temp_seasonal is not None else None,
                "co2_seasonal_strength": float(np.std(co2_seasonal)) if co2_seasonal is not None else None
            }
        }
        
        # Create evidence
        evidence = {
            "data_length": len(df),
            "temp_data_length": len(temp_data) if temp_data is not None else 0,
            "co2_data_length": len(co2_data) if co2_data is not None else 0,
            "time_span_years": (df['year'].max() - df['year'].min()) if 'year' in df.columns else None
        }
        
        return create_truth_table(
            test_name="climate_trend_analysis",
            pass_fail=pass_fail,
            metrics=metrics,
            evidence=evidence
        )
        
    except Exception as e:
        return create_truth_table(
            test_name="climate_trend_analysis",
            pass_fail={"climate_analysis_complete": False},
            metrics={"error": f"Climate trend analysis failed: {str(e)}"},
            evidence={},
            falsification_notes=f"Analysis failed with error: {str(e)}"
        )

def climate_change_detection(data: np.ndarray, **kwargs) -> Dict[str, Any]:
    """
    Detect climate change signals using statistical tests.
    
    Parameters:
    -----------
    data : np.ndarray
        Climate data array
    **kwargs : Additional parameters
        
    Returns:
    --------
    dict : Climate change detection results
    """
    try:
        # Convert to DataFrame if needed
        if isinstance(data, np.ndarray):
            if data.ndim == 1:
                df = pd.DataFrame({'value': data})
            else:
                df = pd.DataFrame(data, columns=['year', 'month', 'temp_anomaly', 'co2_ppm', 
                                               'sea_level', 'arctic_ice', 'antarctic_ice'])
        else:
            df = data
        
        # Extract temperature data
        if 'temp_anomaly' in df.columns:
            temp_data = df['temp_anomaly'].dropna()
        else:
            temp_data = df.iloc[:, 2] if df.shape[1] > 2 else df.iloc[:, 0]
        
        # Mann-Kendall trend test
        mk_result = None
        mk_trend = None
        mk_p_value = None
        
        if len(temp_data) > 10:
            try:
                from scipy.stats import kendalltau
                tau, mk_p_value = kendalltau(range(len(temp_data)), temp_data)
                mk_trend = "increasing" if tau > 0 else "decreasing" if tau < 0 else "no trend"
                mk_result = {"tau": float(tau), "p_value": float(mk_p_value)}
            except:
                mk_result = None
        
        # Augmented Dickey-Fuller test for stationarity
        adf_result = None
        adf_stationary = None
        
        if len(temp_data) > 20:
            try:
                adf_stat, adf_p_value, adf_critical_values, adf_icbest, adf_resstore = adfuller(temp_data)
                adf_stationary = adf_p_value < 0.05
                adf_result = {
                    "adf_statistic": float(adf_stat),
                    "p_value": float(adf_p_value),
                    "critical_values": {str(k): float(v) for k, v in adf_critical_values.items()}
                }
            except:
                adf_result = None
        
        # Breakpoint detection (simple approach)
        breakpoints = []
        if len(temp_data) > 30:
            # Simple breakpoint detection using rolling mean difference
            window = min(10, len(temp_data) // 3)
            rolling_mean = temp_data.rolling(window=window, center=True).mean()
            diff = temp_data - rolling_mean
            threshold = 2 * np.std(diff.dropna())
            breakpoints = np.where(np.abs(diff) > threshold)[0].tolist()
        
        # Pass/fail criteria
        pass_fail = {
            "trend_detected": bool(mk_result is not None),
            "trend_significant": bool(mk_p_value is not None and mk_p_value < 0.05),
            "warming_detected": bool(mk_trend == "increasing"),
            "stationarity_tested": bool(adf_result is not None),
            "non_stationary": bool(adf_stationary is not None and not adf_stationary),
            "breakpoints_detected": bool(len(breakpoints) > 0)
        }
        
        # Create metrics
        metrics = {
            "mann_kendall_test": mk_result,
            "augmented_dickey_fuller": adf_result,
            "breakpoint_analysis": {
                "num_breakpoints": len(breakpoints),
                "breakpoint_positions": breakpoints,
                "detection_threshold": float(threshold) if len(temp_data) > 30 else None
            },
            "trend_summary": {
                "trend_direction": mk_trend,
                "trend_strength": float(abs(tau)) if mk_result else None,
                "significance_level": float(mk_p_value) if mk_p_value else None
            }
        }
        
        # Create evidence
        evidence = {
            "data_length": len(temp_data),
            "time_span": len(temp_data),
            "data_range": float(temp_data.max() - temp_data.min()) if len(temp_data) > 0 else None,
            "data_variance": float(temp_data.var()) if len(temp_data) > 0 else None
        }
        
        return create_truth_table(
            test_name="climate_change_detection",
            pass_fail=pass_fail,
            metrics=metrics,
            evidence=evidence
        )
        
    except Exception as e:
        return create_truth_table(
            test_name="climate_change_detection",
            pass_fail={"climate_change_detection_complete": False},
            metrics={"error": f"Climate change detection failed: {str(e)}"},
            evidence={},
            falsification_notes=f"Analysis failed with error: {str(e)}"
        )

def seasonal_climate_analysis(data: np.ndarray, **kwargs) -> Dict[str, Any]:
    """
    Analyze seasonal patterns in climate data.
    
    Parameters:
    -----------
    data : np.ndarray
        Climate data array
    **kwargs : Additional parameters
        
    Returns:
    --------
    dict : Seasonal climate analysis results
    """
    try:
        # Convert to DataFrame if needed
        if isinstance(data, np.ndarray):
            if data.ndim == 1:
                df = pd.DataFrame({'value': data})
            else:
                df = pd.DataFrame(data, columns=['year', 'month', 'temp_anomaly', 'co2_ppm', 
                                               'sea_level', 'arctic_ice', 'antarctic_ice'])
        else:
            df = data
        
        # Extract temperature data
        if 'temp_anomaly' in df.columns:
            temp_data = df['temp_anomaly'].dropna()
        else:
            temp_data = df.iloc[:, 2] if df.shape[1] > 2 else df.iloc[:, 0]
        
        # Seasonal decomposition
        seasonal_strength = None
        trend_strength = None
        residual_strength = None
        seasonal_pattern = None
        
        if len(temp_data) > 24:  # At least 2 years of monthly data
            try:
                decomposition = seasonal_decompose(temp_data, period=12, extrapolate_trend='freq')
                
                # Calculate strength metrics
                seasonal_strength = np.std(decomposition.seasonal) / np.std(temp_data)
                trend_strength = np.std(decomposition.trend.dropna()) / np.std(temp_data)
                residual_strength = np.std(decomposition.resid.dropna()) / np.std(temp_data)
                
                # Identify seasonal pattern
                seasonal_values = decomposition.seasonal[:12]  # First year
                peak_month = np.argmax(seasonal_values) + 1
                trough_month = np.argmin(seasonal_values) + 1
                
                seasonal_pattern = {
                    "peak_month": int(peak_month),
                    "trough_month": int(trough_month),
                    "amplitude": float(np.max(seasonal_values) - np.min(seasonal_values)),
                    "seasonal_strength": float(seasonal_strength),
                    "trend_strength": float(trend_strength),
                    "residual_strength": float(residual_strength)
                }
            except:
                seasonal_pattern = None
        
        # Monthly statistics
        monthly_stats = None
        if 'month' in df.columns and len(temp_data) > 12:
            monthly_means = temp_data.groupby(df['month']).mean()
            monthly_stds = temp_data.groupby(df['month']).std()
            
            monthly_stats = {
                "monthly_means": monthly_means.to_dict(),
                "monthly_stds": monthly_stds.to_dict(),
                "annual_cycle_amplitude": float(monthly_means.max() - monthly_means.min())
            }
        
        # Pass/fail criteria
        pass_fail = {
            "seasonal_decomposition_successful": bool(seasonal_pattern is not None),
            "strong_seasonal_pattern": bool(seasonal_strength is not None and seasonal_strength > CLIMATE_THRESHOLDS["seasonal_strength_threshold"]),
            "trend_dominates_seasonality": bool(trend_strength is not None and trend_strength > seasonal_strength),
            "monthly_statistics_available": bool(monthly_stats is not None)
        }
        
        # Create metrics
        metrics = {
            "seasonal_analysis": seasonal_pattern,
            "monthly_statistics": monthly_stats,
            "decomposition_summary": {
                "seasonal_strength": float(seasonal_strength) if seasonal_strength is not None else None,
                "trend_strength": float(trend_strength) if trend_strength is not None else None,
                "residual_strength": float(residual_strength) if residual_strength is not None else None
            }
        }
        
        # Create evidence
        evidence = {
            "data_length": len(temp_data),
            "has_monthly_data": 'month' in df.columns,
            "time_span_years": len(temp_data) / 12 if len(temp_data) > 0 else 0
        }
        
        return create_truth_table(
            test_name="seasonal_climate_analysis",
            pass_fail=pass_fail,
            metrics=metrics,
            evidence=evidence
        )
        
    except Exception as e:
        return create_truth_table(
            test_name="seasonal_climate_analysis",
            pass_fail={"seasonal_analysis_complete": False},
            metrics={"error": f"Seasonal climate analysis failed: {str(e)}"},
            evidence={},
            falsification_notes=f"Analysis failed with error: {str(e)}"
        )

def get_climate_functions() -> Dict[str, callable]:
    """Get all climate analysis functions."""
    return {
        "climate_trend_analysis": climate_trend_analysis,
        "climate_change_detection": climate_change_detection,
        "seasonal_climate_analysis": seasonal_climate_analysis
    } 