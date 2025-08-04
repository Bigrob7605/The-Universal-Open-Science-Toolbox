#!/usr/bin/env python3
"""
Seismology Domain - Loaded-Dice Seismic Risk Model
Universal Open Science Toolbox

Implements the Loaded-Dice Seismic Risk Model for analyzing anthropogenic
heat effects on seismic risk, including HWCI (Heat-Warning Correlation Index),
stress perturbation calculations, and observability filters.

Author: Universal Open Science Toolbox
License: MIT
Version: 1.0 - Seismology Domain
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple, List
from scipy import stats
from scipy.spatial.distance import cdist
import warnings
warnings.filterwarnings('ignore')

# Seismology-specific thresholds (Loaded-Dice Model v1.6)
SEISMOLOGY_THRESHOLDS = {
    "hwci_concordance_threshold": 0.8,  # 80% overlap for HWCI hotspots
    "stress_perturbation_min": 1.5,  # kPa minimum for observability
    "fault_depth_cutoff": 4.0,  # km - only faults ≤ 4 km are scored
    "critical_stress_drop": 5.0,  # MPa for M 4-5.5 crustal events
    "heat_flux_sensitivity": 0.5,  # ±50% heat-flux sensitivity toggle
    "rupture_probability_threshold": 0.003,  # ≤ 0.3% advance for M < 5.5
    "observability_noise_floor": 0.5,  # mm for GNSS + strainmeter noise
    "depth_conductive_range": 4.0,  # km - thermo-elastic signal range
    "thermal_conductivity": 1.2e-6,  # m² s⁻¹ for finite-element model
    "waste_heat_threshold": 50.0,  # MW minimum for data center clusters
    "solar_kp_threshold": 7.0,  # Kp index for solar geomagnetic events
    "sea_level_rise_rate": 3.0,  # mm/year global average
    "extreme_rainfall_threshold": 100.0,  # mm/day for pore-pressure effects
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

def heat_warning_correlation_index(data: np.ndarray, **kwargs) -> Dict[str, Any]:
    """
    Calculate Heat-Warning Correlation Index (HWCI v2.0).
    
    Overlays NOAA heat-warning polygons with ≥ 50 MW data-center clusters
    to identify anthropogenic heat hotspots that may affect seismic risk.
    
    Parameters:
    -----------
    data : np.ndarray
        Array containing [latitude, longitude, heat_warning_status, data_center_mw, ...]
    **kwargs : Additional parameters
        
    Returns:
    --------
    dict : HWCI analysis results
    """
    try:
        # Convert to DataFrame if needed
        if isinstance(data, np.ndarray):
            if data.ndim == 1:
                # Single location data
                df = pd.DataFrame({
                    'lat': [data[0]] if len(data) > 0 else [0],
                    'lon': [data[1]] if len(data) > 1 else [0],
                    'heat_warning': [data[2]] if len(data) > 2 else [0],
                    'data_center_mw': [data[3]] if len(data) > 3 else [0]
                })
            else:
                # Multi-location data
                df = pd.DataFrame(data, columns=['lat', 'lon', 'heat_warning', 'data_center_mw'])
        else:
            df = data
        
        # Calculate HWCI metrics
        total_locations = len(df)
        heat_warning_locations = len(df[df['heat_warning'] > 0])
        data_center_locations = len(df[df['data_center_mw'] >= SEISMOLOGY_THRESHOLDS["waste_heat_threshold"]])
        
        # Find overlap (locations with both heat warnings and data centers)
        overlap_locations = len(df[(df['heat_warning'] > 0) & 
                                 (df['data_center_mw'] >= SEISMOLOGY_THRESHOLDS["waste_heat_threshold"])])
        
        # Calculate concordance percentage
        if total_locations > 0:
            concordance_percentage = (overlap_locations / total_locations) * 100
        else:
            concordance_percentage = 0
        
        # Calculate total waste heat in MW
        total_waste_heat = df['data_center_mw'].sum()
        
        # Identify top hotspots (locations with highest combined risk)
        df['combined_risk'] = df['heat_warning'] * df['data_center_mw']
        top_hotspots = df.nlargest(5, 'combined_risk')[['lat', 'lon', 'combined_risk']].to_dict('records')
        
        # Pass/fail criteria
        pass_fail = {
            "data_loaded": True,
            "hwci_above_threshold": concordance_percentage >= (SEISMOLOGY_THRESHOLDS["hwci_concordance_threshold"] * 100),
            "significant_waste_heat": total_waste_heat >= 1000,  # 1 GW total
            "multiple_hotspots": len(top_hotspots) >= 3,
            "observability_filter": concordance_percentage >= 70  # 70% concordance for observability
        }
        
        metrics = {
            "total_locations": total_locations,
            "heat_warning_locations": heat_warning_locations,
            "data_center_locations": data_center_locations,
            "overlap_locations": overlap_locations,
            "concordance_percentage": concordance_percentage,
            "total_waste_heat_mw": total_waste_heat,
            "top_hotspots": top_hotspots,
            "hwci_version": "2.0"
        }
        
        evidence = {
            "heat_warning_coverage": f"{heat_warning_locations}/{total_locations} locations under heat warnings",
            "data_center_coverage": f"{data_center_locations}/{total_locations} locations with ≥{SEISMOLOGY_THRESHOLDS['waste_heat_threshold']} MW",
            "overlap_analysis": f"{overlap_locations} locations show both heat warnings and data centers",
            "risk_assessment": "High overlap indicates potential anthropogenic heat effects on seismic risk"
        }
        
        return create_truth_table(
            "heat_warning_correlation_index",
            pass_fail,
            metrics,
            evidence,
            "HWCI analysis completed successfully"
        )
        
    except Exception as e:
        return create_truth_table(
            "heat_warning_correlation_index",
            {"data_loaded": False, "analysis_failed": True},
            {"error": str(e)},
            {},
            f"HWCI analysis failed: {str(e)}"
        )

def stress_perturbation_analysis(data: np.ndarray, **kwargs) -> Dict[str, Any]:
    """
    Calculate stress perturbation (Δσ) from anthropogenic heat sources.
    
    Implements the Loaded-Dice model for quantifying sub-critical anthropogenic
    stress perturbations on urban faults.
    
    Parameters:
    -----------
    data : np.ndarray
        Array containing [depth_km, heat_flux_mw_km2, fault_depth_km, ...]
    **kwargs : Additional parameters
        
    Returns:
    --------
    dict : Stress perturbation analysis results
    """
    try:
        # Convert to DataFrame if needed
        if isinstance(data, np.ndarray):
            if data.ndim == 1:
                # Single location data
                df = pd.DataFrame({
                    'depth_km': [data[0]] if len(data) > 0 else [0.1],
                    'heat_flux_mw_km2': [data[1]] if len(data) > 1 else [10],
                    'fault_depth_km': [data[2]] if len(data) > 2 else [2.0],
                    'thermal_conductivity': [data[3]] if len(data) > 3 else [SEISMOLOGY_THRESHOLDS["thermal_conductivity"]]
                })
            else:
                # Multi-location data
                df = pd.DataFrame(data, columns=['depth_km', 'heat_flux_mw_km2', 'fault_depth_km', 'thermal_conductivity'])
        else:
            df = data
        
        # Apply depth cut-off filter (only faults ≤ 4 km)
        df_filtered = df[df['fault_depth_km'] <= SEISMOLOGY_THRESHOLDS["fault_depth_cutoff"]]
        
        if len(df_filtered) == 0:
            return create_truth_table(
                "stress_perturbation_analysis",
                {"data_loaded": False, "no_valid_faults": True},
                {"error": "No faults within depth cut-off range"},
                {},
                "All faults exceed 4 km depth cut-off"
            )
        
        # Calculate stress perturbation using thermo-elastic model
        # Δσ = α * E * ΔT / (1 - ν) where α is thermal expansion, E is Young's modulus
        # Simplified model: Δσ ≈ heat_flux * depth_factor * conductivity_factor
        
        # Depth factor (decreases with depth)
        depth_factor = np.exp(-df_filtered['depth_km'] / 2.0)
        
        # Heat flux factor (MW/km² to stress perturbation)
        heat_factor = df_filtered['heat_flux_mw_km2'] * 0.1  # Simplified conversion
        
        # Calculate Δσ for each location
        delta_sigma = heat_factor * depth_factor * df_filtered['thermal_conductivity'] * 1e6  # Convert to Pa
        
        # Calculate statistics
        mean_delta_sigma = np.mean(delta_sigma)
        std_delta_sigma = np.std(delta_sigma)
        max_delta_sigma = np.max(delta_sigma)
        min_delta_sigma = np.min(delta_sigma)
        
        # Calculate 90% confidence intervals using Monte Carlo simulation
        n_simulations = 1000
        mc_results = []
        for _ in range(n_simulations):
            # Add uncertainty to heat flux (±50%)
            uncertainty_factor = np.random.normal(1.0, 0.2)  # 20% standard deviation
            mc_delta_sigma = heat_factor * depth_factor * df_filtered['thermal_conductivity'] * 1e6 * uncertainty_factor
            mc_results.append(np.mean(mc_delta_sigma))
        
        mc_results = np.array(mc_results)
        ci_90_lower = np.percentile(mc_results, 5)
        ci_90_upper = np.percentile(mc_results, 95)
        
        # Calculate rupture probability shift
        # λ(t) = λ₀(t) · [1 + ε_heat(t)] where ε_heat(t) ~ 𝒩(μ = Δσ/σ_crit, σ = 0.2·μ)
        sigma_crit = SEISMOLOGY_THRESHOLDS["critical_stress_drop"] * 1e6  # Convert MPa to Pa
        epsilon_heat = mean_delta_sigma / sigma_crit
        rupture_probability_shift = epsilon_heat * 100  # Convert to percentage
        
        # Observability filter
        noise_floor = SEISMOLOGY_THRESHOLDS["observability_noise_floor"] * 1e-3  # Convert mm to m
        observability_threshold = 1.5 * noise_floor
        observability_filter = mean_delta_sigma >= observability_threshold
        
        # Pass/fail criteria
        pass_fail = {
            "data_loaded": True,
            "valid_faults_present": len(df_filtered) > 0,
            "stress_above_observability": mean_delta_sigma >= SEISMOLOGY_THRESHOLDS["stress_perturbation_min"] * 1000,  # Convert kPa to Pa
            "rupture_probability_acceptable": rupture_probability_shift <= SEISMOLOGY_THRESHOLDS["rupture_probability_threshold"] * 100,
            "observability_filter_passed": observability_filter,
            "depth_cutoff_applied": len(df_filtered) < len(df)
        }
        
        metrics = {
            "mean_delta_sigma_pa": mean_delta_sigma,
            "std_delta_sigma_pa": std_delta_sigma,
            "max_delta_sigma_pa": max_delta_sigma,
            "min_delta_sigma_pa": min_delta_sigma,
            "ci_90_lower_pa": ci_90_lower,
            "ci_90_upper_pa": ci_90_upper,
            "rupture_probability_shift_percent": rupture_probability_shift,
            "observability_threshold_pa": observability_threshold,
            "valid_fault_count": len(df_filtered),
            "total_fault_count": len(df),
            "sigma_crit_pa": sigma_crit
        }
        
        evidence = {
            "depth_analysis": f"{len(df_filtered)}/{len(df)} faults within {SEISMOLOGY_THRESHOLDS['fault_depth_cutoff']} km depth",
            "stress_range": f"Δσ range: {min_delta_sigma/1000:.1f} - {max_delta_sigma/1000:.1f} kPa",
            "confidence_interval": f"90% CI: {ci_90_lower/1000:.1f} - {ci_90_upper/1000:.1f} kPa",
            "rupture_effect": f"Predicted rupture probability shift: {rupture_probability_shift:.3f}%",
            "observability_status": f"Observability filter: {'PASS' if observability_filter else 'FAIL'}"
        }
        
        return create_truth_table(
            "stress_perturbation_analysis",
            pass_fail,
            metrics,
            evidence,
            "Stress perturbation analysis completed successfully"
        )
        
    except Exception as e:
        return create_truth_table(
            "stress_perturbation_analysis",
            {"data_loaded": False, "analysis_failed": True},
            {"error": str(e)},
            {},
            f"Stress perturbation analysis failed: {str(e)}"
        )

def seismic_modulator_analysis(data: np.ndarray, **kwargs) -> Dict[str, Any]:
    """
    Analyze multiple seismic modulators (solar, climatic, anthropogenic).
    
    Implements the Loaded-Dice modulator catalogue for quantifying
    non-tectonic processes that may affect seismic risk.
    
    Parameters:
    -----------
    data : np.ndarray
        Array containing modulator data [solar_kp, rainfall_mm, sea_level_mm, waste_heat_mw, ...]
    **kwargs : Additional parameters
        
    Returns:
    --------
    dict : Seismic modulator analysis results
    """
    try:
        # Convert to DataFrame if needed
        if isinstance(data, np.ndarray):
            if data.ndim == 1:
                # Single time point data
                df = pd.DataFrame({
                    'solar_kp': [data[0]] if len(data) > 0 else [2.0],
                    'rainfall_mm': [data[1]] if len(data) > 1 else [10.0],
                    'sea_level_mm': [data[2]] if len(data) > 2 else [0.0],
                    'waste_heat_mw': [data[3]] if len(data) > 3 else [100.0],
                    'gia_uplift_mm': [data[4]] if len(data) > 4 else [0.0]
                })
            else:
                # Multi-time point data
                df = pd.DataFrame(data, columns=['solar_kp', 'rainfall_mm', 'sea_level_mm', 'waste_heat_mw', 'gia_uplift_mm'])
        else:
            df = data
        
        # Calculate modulator effects
        modulator_effects = {}
        
        # 1. Solar geomagnetic pulses (Kp index)
        solar_events = df[df['solar_kp'] >= SEISMOLOGY_THRESHOLDS["solar_kp_threshold"]]
        solar_delta_sigma = len(solar_events) * 0.5  # 0.5 kPa per Kp ≥ 7 event
        modulator_effects["solar_geomagnetic"] = {
            "delta_sigma_kpa": solar_delta_sigma,
            "event_count": len(solar_events),
            "evidence_quality": "Moderate",
            "observability": len(solar_events) > 0
        }
        
        # 2. Extreme rainfall (pore-pressure diffusion)
        extreme_rainfall = df[df['rainfall_mm'] >= SEISMOLOGY_THRESHOLDS["extreme_rainfall_threshold"]]
        rainfall_delta_sigma = len(extreme_rainfall) * 2.0  # 2 kPa per extreme rainfall event
        modulator_effects["extreme_rainfall"] = {
            "delta_sigma_kpa": rainfall_delta_sigma,
            "event_count": len(extreme_rainfall),
            "evidence_quality": "Moderate",
            "observability": len(extreme_rainfall) > 0
        }
        
        # 3. Sea-level rise (ocean flexure)
        sea_level_rate = np.mean(df['sea_level_mm']) / 1000  # Convert to m/year
        sea_level_delta_sigma = sea_level_rate * SEISMOLOGY_THRESHOLDS["sea_level_rise_rate"] * 0.1  # 0.1 kPa per mm/year
        modulator_effects["sea_level_rise"] = {
            "delta_sigma_kpa": sea_level_delta_sigma,
            "rate_mm_per_year": sea_level_rate * 1000,
            "evidence_quality": "Moderate",
            "observability": sea_level_rate > 0
        }
        
        # 4. Data center waste heat (thermo-elastic expansion)
        total_waste_heat = df['waste_heat_mw'].sum()
        waste_heat_delta_sigma = total_waste_heat * 0.01  # 0.01 kPa per MW
        modulator_effects["data_center_waste_heat"] = {
            "delta_sigma_kpa": waste_heat_delta_sigma,
            "total_mw": total_waste_heat,
            "evidence_quality": "Emerging",
            "observability": total_waste_heat >= 1000  # 1 GW threshold
        }
        
        # 5. Glacial Isostatic Adjustment (GIA)
        gia_uplift_rate = np.mean(df['gia_uplift_mm']) / 1000  # Convert to m/year
        gia_delta_sigma = gia_uplift_rate * 3.0  # 3 kPa per mm/year uplift
        modulator_effects["gia"] = {
            "delta_sigma_kpa": gia_delta_sigma,
            "uplift_rate_mm_per_year": gia_uplift_rate * 1000,
            "evidence_quality": "High",
            "observability": abs(gia_uplift_rate) > 0.001  # 1 mm/year threshold
        }
        
        # Calculate total modulator effect
        total_delta_sigma = sum(mod["delta_sigma_kpa"] for mod in modulator_effects.values())
        
        # Calculate combined probability shift
        sigma_crit = SEISMOLOGY_THRESHOLDS["critical_stress_drop"] * 1000  # Convert MPa to kPa
        combined_probability_shift = (total_delta_sigma / sigma_crit) * 100
        
        # Pass/fail criteria
        pass_fail = {
            "data_loaded": True,
            "multiple_modulators_present": len(modulator_effects) >= 3,
            "significant_total_effect": total_delta_sigma >= 5.0,  # 5 kPa total effect
            "probability_shift_acceptable": combined_probability_shift <= 1.0,  # ≤ 1% total shift
            "observable_modulators": sum(1 for mod in modulator_effects.values() if mod["observability"]) >= 2
        }
        
        metrics = {
            "total_delta_sigma_kpa": total_delta_sigma,
            "combined_probability_shift_percent": combined_probability_shift,
            "modulator_count": len(modulator_effects),
            "observable_modulator_count": sum(1 for mod in modulator_effects.values() if mod["observability"]),
            "sigma_crit_kpa": sigma_crit,
            "modulator_effects": modulator_effects
        }
        
        evidence = {
            "modulator_summary": f"Analyzed {len(modulator_effects)} seismic modulators",
            "total_effect": f"Combined Δσ: {total_delta_sigma:.1f} kPa",
            "probability_impact": f"Combined probability shift: {combined_probability_shift:.3f}%",
            "observability_status": f"{sum(1 for mod in modulator_effects.values() if mod['observability'])} modulators observable"
        }
        
        return create_truth_table(
            "seismic_modulator_analysis",
            pass_fail,
            metrics,
            evidence,
            "Seismic modulator analysis completed successfully"
        )
        
    except Exception as e:
        return create_truth_table(
            "seismic_modulator_analysis",
            {"data_loaded": False, "analysis_failed": True},
            {"error": str(e)},
            {},
            f"Seismic modulator analysis failed: {str(e)}"
        )

def get_seismology_functions() -> Dict[str, callable]:
    """Get all seismology domain functions."""
    return {
        "heat_warning_correlation_index": heat_warning_correlation_index,
        "stress_perturbation_analysis": stress_perturbation_analysis,
        "seismic_modulator_analysis": seismic_modulator_analysis
    } 