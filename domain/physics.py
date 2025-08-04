"""
Physics Domain Tests for Universal Open Science Toolbox
LIGO strain analysis and SNR thresholds
"""

import numpy as np
from scipy import stats
from scipy.signal import find_peaks
from typing import Dict, Any, Optional
import warnings

# Physics-specific thresholds
PHYSICS_THRESHOLDS = {
    "ligo_snr_threshold": 8.0,  # LIGO detection threshold
    "gravitational_wave_frequency_range": (20, 2000),  # Hz
    "strain_sensitivity": 1e-21,  # LIGO strain sensitivity
    "signal_duration_min": 0.1,  # seconds
    "signal_duration_max": 10.0,  # seconds
    "chirp_mass_range": (1.0, 100.0),  # solar masses
    "merger_rate_threshold": 1e-6  # events per year per Mpc^3
}

def ligo_strain_analysis(data: np.ndarray, **kwargs) -> Dict[str, Any]:
    """
    LIGO gravitational wave strain analysis.
    
    Parameters:
    -----------
    data : np.ndarray
        Strain data (time series)
    sample_rate : float, optional
        Sampling rate in Hz (default: 4096 Hz)
    **kwargs : Additional parameters
        
    Returns:
    --------
    dict : LIGO strain analysis results with pass/fail criteria
    """
    try:
        # Ensure data is 1D
        if data.ndim > 1:
            data_flat = data.flatten()
        else:
            data_flat = data
        
        sample_rate = kwargs.get('sample_rate', 4096.0)
        snr_threshold = kwargs.get('snr_threshold', PHYSICS_THRESHOLDS["ligo_snr_threshold"])
        
        # Time domain analysis
        time_domain = {
            "duration": len(data_flat) / sample_rate,
            "mean_strain": float(np.mean(data_flat)),
            "std_strain": float(np.std(data_flat)),
            "max_strain": float(np.max(np.abs(data_flat))),
            "rms_strain": float(np.sqrt(np.mean(data_flat**2)))
        }
        
        # Frequency domain analysis
        fft = np.fft.fft(data_flat)
        freqs = np.fft.fftfreq(len(data_flat), 1/sample_rate)
        power_spectrum = np.abs(fft)**2
        
        # Find dominant frequency
        positive_freqs = freqs[freqs > 0]
        positive_power = power_spectrum[freqs > 0]
        if len(positive_power) > 0:
            dominant_freq_idx = np.argmax(positive_power)
            dominant_frequency = positive_freqs[dominant_freq_idx]
        else:
            dominant_frequency = 0
        
        # SNR calculation (simplified)
        signal_power = np.max(power_spectrum)
        noise_power = np.mean(power_spectrum)
        snr = np.sqrt(signal_power / noise_power) if noise_power > 0 else 0
        
        # Peak detection for gravitational wave candidates
        peaks, properties = find_peaks(np.abs(data_flat), 
                                     height=np.std(data_flat) * 3,
                                     distance=int(sample_rate * 0.1))
        
        # Pass/fail criteria
        pass_fail = {
            "data_loaded": True,
            "snr_above_threshold": snr > snr_threshold,
            "frequency_in_range": (PHYSICS_THRESHOLDS["gravitational_wave_frequency_range"][0] <= 
                                 dominant_frequency <= 
                                 PHYSICS_THRESHOLDS["gravitational_wave_frequency_range"][1]),
            "duration_appropriate": (PHYSICS_THRESHOLDS["signal_duration_min"] <= 
                                  time_domain["duration"] <= 
                                  PHYSICS_THRESHOLDS["signal_duration_max"]),
            "peaks_detected": len(peaks) > 0,
            "strain_sensitivity_adequate": time_domain["rms_strain"] > PHYSICS_THRESHOLDS["strain_sensitivity"]
        }
        
        return {
            "time_domain_analysis": time_domain,
            "frequency_domain_analysis": {
                "dominant_frequency": float(dominant_frequency),
                "frequency_range": PHYSICS_THRESHOLDS["gravitational_wave_frequency_range"],
                "power_spectrum_max": float(np.max(power_spectrum)),
                "power_spectrum_mean": float(np.mean(power_spectrum))
            },
            "snr_analysis": {
                "snr": float(snr),
                "snr_threshold": float(snr_threshold),
                "signal_power": float(signal_power),
                "noise_power": float(noise_power)
            },
            "peak_analysis": {
                "num_peaks": int(len(peaks)),
                "peak_positions": peaks.tolist(),
                "peak_heights": data_flat[peaks].tolist() if len(peaks) > 0 else []
            },
            "detection_summary": {
                "gravitational_wave_candidate": (pass_fail["snr_above_threshold"] and 
                                              pass_fail["frequency_in_range"] and 
                                              pass_fail["peaks_detected"]),
                "signal_quality": "high" if snr > 10 else "medium" if snr > 5 else "low"
            },
            "pass_fail": pass_fail
        }
        
    except Exception as e:
        return {
            "error": f"LIGO strain analysis failed: {str(e)}",
            "pass_fail": {"data_loaded": False}
        }

def particle_physics_analysis(data: np.ndarray, **kwargs) -> Dict[str, Any]:
    """
    Particle physics data analysis.
    
    Parameters:
    -----------
    data : np.ndarray
        Particle collision data (energy, momentum, etc.)
    **kwargs : Additional parameters
        
    Returns:
    --------
    dict : Particle physics analysis results with pass/fail criteria
    """
    try:
        # Ensure data is 2D
        if data.ndim == 1:
            data_2d = data.reshape(-1, 1)
        else:
            data_2d = data
        
        # Energy analysis
        if data_2d.shape[1] >= 1:
            energy_data = data_2d[:, 0]
            energy_stats = {
                "mean_energy": float(np.mean(energy_data)),
                "std_energy": float(np.std(energy_data)),
                "max_energy": float(np.max(energy_data)),
                "min_energy": float(np.min(energy_data))
            }
        else:
            energy_stats = {}
        
        # Momentum analysis (if available)
        if data_2d.shape[1] >= 3:
            momentum_data = data_2d[:, 1:4]
            momentum_magnitudes = np.sqrt(np.sum(momentum_data**2, axis=1))
            momentum_stats = {
                "mean_momentum": float(np.mean(momentum_magnitudes)),
                "std_momentum": float(np.std(momentum_magnitudes)),
                "max_momentum": float(np.max(momentum_magnitudes))
            }
        else:
            momentum_stats = {}
        
        # Invariant mass calculation (if we have 4-momentum)
        if data_2d.shape[1] >= 4:
            energy = data_2d[:, 0]
            px = data_2d[:, 1]
            py = data_2d[:, 2]
            pz = data_2d[:, 3]
            
            # E^2 - p^2 = m^2
            invariant_masses = np.sqrt(energy**2 - (px**2 + py**2 + pz**2))
            invariant_mass_stats = {
                "mean_mass": float(np.mean(invariant_masses)),
                "std_mass": float(np.std(invariant_masses)),
                "mass_range": [float(np.min(invariant_masses)), float(np.max(invariant_masses))]
            }
        else:
            invariant_mass_stats = {}
        
        # Pass/fail criteria
        pass_fail = {
            "data_loaded": True,
            "energy_analysis_complete": len(energy_stats) > 0,
            "momentum_analysis_complete": len(momentum_stats) > 0,
            "mass_analysis_complete": len(invariant_mass_stats) > 0,
            "data_quality_adequate": len(data_2d) > 100
        }
        
        return {
            "energy_analysis": energy_stats,
            "momentum_analysis": momentum_stats,
            "invariant_mass_analysis": invariant_mass_stats,
            "data_summary": {
                "num_events": int(len(data_2d)),
                "num_observables": int(data_2d.shape[1]),
                "data_completeness": "full" if data_2d.shape[1] >= 4 else "partial"
            },
            "pass_fail": pass_fail
        }
        
    except Exception as e:
        return {
            "error": f"Particle physics analysis failed: {str(e)}",
            "pass_fail": {"data_loaded": False}
        }

def cosmology_analysis(data: np.ndarray, **kwargs) -> Dict[str, Any]:
    """
    Cosmological data analysis.
    
    Parameters:
    -----------
    data : np.ndarray
        Cosmological data (redshift, distance, etc.)
    **kwargs : Additional parameters
        
    Returns:
    --------
    dict : Cosmology analysis results with pass/fail criteria
    """
    try:
        # Ensure data is 2D
        if data.ndim == 1:
            data_2d = data.reshape(-1, 1)
        else:
            data_2d = data
        
        # Redshift analysis
        if data_2d.shape[1] >= 1:
            redshift_data = data_2d[:, 0]
            redshift_stats = {
                "mean_redshift": float(np.mean(redshift_data)),
                "std_redshift": float(np.std(redshift_data)),
                "max_redshift": float(np.max(redshift_data)),
                "min_redshift": float(np.min(redshift_data))
            }
        else:
            redshift_stats = {}
        
        # Distance analysis (if available)
        if data_2d.shape[1] >= 2:
            distance_data = data_2d[:, 1]
            distance_stats = {
                "mean_distance": float(np.mean(distance_data)),
                "std_distance": float(np.std(distance_data)),
                "max_distance": float(np.max(distance_data)),
                "min_distance": float(np.min(distance_data))
            }
        else:
            distance_stats = {}
        
        # Hubble diagram analysis (if we have both redshift and distance)
        if data_2d.shape[1] >= 2:
            redshift = data_2d[:, 0]
            distance = data_2d[:, 1]
            
            # Calculate Hubble parameter H = v/d = cz/d
            c = 299792.458  # km/s
            hubble_parameters = c * redshift / distance
            hubble_stats = {
                "mean_hubble_parameter": float(np.mean(hubble_parameters)),
                "std_hubble_parameter": float(np.std(hubble_parameters)),
                "hubble_constant_estimate": float(np.mean(hubble_parameters))
            }
        else:
            hubble_stats = {}
        
        # Pass/fail criteria
        pass_fail = {
            "data_loaded": True,
            "redshift_analysis_complete": len(redshift_stats) > 0,
            "distance_analysis_complete": len(distance_stats) > 0,
            "hubble_analysis_complete": len(hubble_stats) > 0,
            "data_quality_adequate": len(data_2d) > 50
        }
        
        return {
            "redshift_analysis": redshift_stats,
            "distance_analysis": distance_stats,
            "hubble_analysis": hubble_stats,
            "cosmology_summary": {
                "num_galaxies": int(len(data_2d)),
                "redshift_range": [float(np.min(redshift_data)), float(np.max(redshift_data))] if len(redshift_stats) > 0 else [],
                "distance_range": [float(np.min(distance_data)), float(np.max(distance_data))] if len(distance_stats) > 0 else []
            },
            "pass_fail": pass_fail
        }
        
    except Exception as e:
        return {
            "error": f"Cosmology analysis failed: {str(e)}",
            "pass_fail": {"data_loaded": False}
        }

# Available physics tests
PHYSICS_TESTS = {
    "ligo_strain_analysis": ligo_strain_analysis,
    "particle_physics_analysis": particle_physics_analysis,
    "cosmology_analysis": cosmology_analysis
}

def get_physics_tests() -> Dict[str, str]:
    """Get list of available physics test functions with descriptions."""
    return {
        "ligo_strain_analysis": "LIGO gravitational wave strain analysis with SNR thresholds",
        "particle_physics_analysis": "Particle collision data analysis (energy, momentum, mass)",
        "cosmology_analysis": "Cosmological data analysis (redshift, distance, Hubble parameter)"
    } 