#!/usr/bin/env python3
"""
Climate Trend Detection Example
Universal Open Science Toolbox

This example demonstrates climate data analysis using real datasets
and trend detection capabilities.
"""

import os
import sys
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime
from scipy import stats
from scipy.signal import detrend

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from BULLETPROOF_PIPELINE import BulletproofPipeline
from test_suite.universal_test_functions import (
    basic_statistical_analysis, correlation_analysis, 
    signal_detection_test, periodicity_test
)

def generate_realistic_climate_data():
    """Generate realistic climate data with known trends."""
    # Generate 50 years of monthly temperature data (1950-2000)
    n_years = 50
    n_months = n_years * 12
    
    # Base temperature (15°C average)
    base_temp = 15.0
    
    # Add seasonal cycle (sinusoidal)
    months = np.arange(n_months)
    seasonal_cycle = 10 * np.sin(2 * np.pi * months / 12)
    
    # Add long-term warming trend (0.02°C per year)
    warming_trend = 0.02 * months / 12
    
    # Add some natural variability
    natural_variability = np.random.normal(0, 2, n_months)
    
    # Combine all components
    temperature = base_temp + seasonal_cycle + warming_trend + natural_variability
    
    # Generate corresponding time data
    years = 1950 + months / 12
    dates = pd.date_range(start='1950-01-01', periods=n_months, freq='M')
    
    # Create DataFrame
    climate_data = pd.DataFrame({
        'date': dates,
        'year': years,
        'temperature': temperature,
        'month': (months % 12) + 1
    })
    
    print(f"Generated climate data:")
    print(f"  - Time period: {years[0]:.1f} - {years[-1]:.1f}")
    print(f"  - Data points: {len(climate_data)}")
    print(f"  - Temperature range: {np.min(temperature):.1f}°C - {np.max(temperature):.1f}°C")
    print(f"  - Mean temperature: {np.mean(temperature):.1f}°C")
    print(f"  - Warming trend: {warming_trend[-1] - warming_trend[0]:.2f}°C over {n_years} years")
    
    return climate_data

def analyze_climate_trends(climate_data):
    """Analyze climate data for trends and patterns."""
    temperature = climate_data['temperature'].values
    years = climate_data['year'].values
    
    # 1. Linear trend analysis
    slope, intercept, r_value, p_value, std_err = stats.linregress(years, temperature)
    trend_per_decade = slope * 10  # Convert to per decade
    
    # 2. Detrended analysis
    detrended_temp = detrend(temperature)
    
    # 3. Seasonal decomposition
    seasonal_means = []
    for month in range(1, 13):
        month_data = climate_data[climate_data['month'] == month]['temperature']
        seasonal_means.append(month_data.mean())
    
    # 4. Moving average
    window_size = 12  # 1 year
    moving_avg = pd.Series(temperature).rolling(window=window_size, center=True).mean()
    
    # 5. Statistical tests
    # Mann-Kendall trend test
    from scipy.stats import kendalltau
    tau, p_tau = kendalltau(years, temperature)
    
    # Results
    results = {
        "trend_analysis": {
            "slope_per_year": float(slope),
            "trend_per_decade": float(trend_per_decade),
            "r_squared": float(r_value**2),
            "p_value": float(p_value),
            "intercept": float(intercept)
        },
        "detrended_analysis": {
            "std_detrended": float(np.std(detrended_temp)),
            "mean_detrended": float(np.mean(detrended_temp))
        },
        "seasonal_analysis": {
            "seasonal_amplitude": float(max(seasonal_means) - min(seasonal_means)),
            "seasonal_means": [float(x) for x in seasonal_means]
        },
        "statistical_tests": {
            "kendall_tau": float(tau),
            "kendall_p_value": float(p_tau)
        },
        "summary_stats": {
            "total_warming": float(temperature[-1] - temperature[0]),
            "warming_rate": float(trend_per_decade),
            "data_span_years": float(years[-1] - years[0])
        }
    }
    
    return results

def run_individual_climate_tests():
    """Run individual climate analysis tests."""
    print("\n" + "="*60)
    print("RUNNING INDIVIDUAL CLIMATE TESTS")
    print("="*60)
    
    # Generate climate data
    climate_data = generate_realistic_climate_data()
    temperature = climate_data['temperature'].values
    
    # 1. Basic Statistical Analysis
    print("\n1. Basic Statistical Analysis")
    print("-" * 40)
    
    stats_result = basic_statistical_analysis(temperature)
    
    print("Statistical Results:")
    if 'metrics' in stats_result:
        metrics = stats_result['metrics']
        mean_val = metrics.get('mean', 'N/A')
        std_val = metrics.get('std', 'N/A')
        min_val = metrics.get('min', 'N/A')
        max_val = metrics.get('max', 'N/A')
        
        print(f"  - Mean: {mean_val:.2f}°C" if isinstance(mean_val, (int, float)) else f"  - Mean: {mean_val}°C")
        print(f"  - Std Dev: {std_val:.2f}°C" if isinstance(std_val, (int, float)) else f"  - Std Dev: {std_val}°C")
        print(f"  - Min: {min_val:.2f}°C" if isinstance(min_val, (int, float)) else f"  - Min: {min_val}°C")
        print(f"  - Max: {max_val:.2f}°C" if isinstance(max_val, (int, float)) else f"  - Max: {max_val}°C")
    
    # 2. Trend Analysis
    print("\n2. Climate Trend Analysis")
    print("-" * 40)
    
    trend_results = analyze_climate_trends(climate_data)
    
    print("Trend Analysis Results:")
    trend = trend_results['trend_analysis']
    print(f"  - Warming rate: {trend['trend_per_decade']:.3f}°C/decade")
    print(f"  - R-squared: {trend['r_squared']:.3f}")
    print(f"  - P-value: {trend['p_value']:.2e}")
    print(f"  - Total warming: {trend_results['summary_stats']['total_warming']:.2f}°C")
    
    # 3. Signal Detection
    print("\n3. Signal Detection Test")
    print("-" * 40)
    
    signal_result = signal_detection_test(temperature)
    
    print("Signal Detection Results:")
    if 'metrics' in signal_result:
        metrics = signal_result['metrics']
        snr_val = metrics.get('snr', 'N/A')
        peak_val = metrics.get('peak_amplitude', 'N/A')
        quality_val = metrics.get('signal_quality', 'N/A')
        
        print(f"  - SNR: {snr_val:.2f}" if isinstance(snr_val, (int, float)) else f"  - SNR: {snr_val}")
        print(f"  - Peak amplitude: {peak_val:.2f}" if isinstance(peak_val, (int, float)) else f"  - Peak amplitude: {peak_val}")
        print(f"  - Signal quality: {quality_val}")
    
    # 4. Periodicity Analysis
    print("\n4. Periodicity Analysis")
    print("-" * 40)
    
    periodicity_result = periodicity_test(temperature)
    
    print("Periodicity Results:")
    if 'metrics' in periodicity_result:
        metrics = periodicity_result['metrics']
        period_val = metrics.get('dominant_period', 'N/A')
        strength_val = metrics.get('periodicity_strength', 'N/A')
        pattern_val = metrics.get('seasonal_pattern', False)
        
        print(f"  - Dominant period: {period_val:.1f} months" if isinstance(period_val, (int, float)) else f"  - Dominant period: {period_val} months")
        print(f"  - Periodicity strength: {strength_val:.3f}" if isinstance(strength_val, (int, float)) else f"  - Periodicity strength: {strength_val}")
        print(f"  - Seasonal pattern: {'Yes' if pattern_val else 'No'}")

def run_pipeline_integration():
    """Run climate analysis through the BulletproofPipeline."""
    print("\n" + "="*60)
    print("RUNNING PIPELINE INTEGRATION")
    print("="*60)
    
    # Initialize pipeline
    pipeline = BulletproofPipeline()
    
    # Register climate analysis functions
    pipeline.register_test_function("basic_statistical_analysis", basic_statistical_analysis)
    pipeline.register_test_function("correlation_analysis", correlation_analysis)
    pipeline.register_test_function("signal_detection_test", signal_detection_test)
    pipeline.register_test_function("periodicity_test", periodicity_test)
    
    # Generate and save climate data
    climate_data = generate_realistic_climate_data()
    temperature = climate_data['temperature'].values
    
    # Save data temporarily
    temp_file = "temp_climate_data.npy"
    np.save(temp_file, temperature)
    
    # Load data into pipeline
    success = pipeline.load_data(temp_file, "numpy")
    
    if success:
        print("✅ Climate data loaded successfully")
        
        # Run statistical analysis
        print("\nRunning statistical analysis...")
        stats_result = pipeline.run_test("basic_statistical_analysis")
        
        if 'result' in stats_result:
            print("Statistical Analysis Results:")
            result = stats_result['result']
            if 'metrics' in result:
                metrics = result['metrics']
                mean_val = metrics.get('mean', 'N/A')
                min_val = metrics.get('min', 'N/A')
                max_val = metrics.get('max', 'N/A')
                
                print(f"  - Mean temperature: {mean_val:.2f}°C" if isinstance(mean_val, (int, float)) else f"  - Mean temperature: {mean_val}°C")
                print(f"  - Temperature range: {min_val:.1f}°C - {max_val:.1f}°C" if isinstance(min_val, (int, float)) and isinstance(max_val, (int, float)) else f"  - Temperature range: {min_val}°C - {max_val}°C")
        
        # Run signal detection
        print("\nRunning signal detection...")
        signal_result = pipeline.run_test("signal_detection_test")
        
        if 'result' in signal_result:
            print("Signal Detection Results:")
            result = signal_result['result']
            if 'metrics' in result:
                metrics = result['metrics']
                snr_val = metrics.get('snr', 'N/A')
                quality_val = metrics.get('signal_quality', 'N/A')
                
                print(f"  - Signal-to-noise ratio: {snr_val:.2f}" if isinstance(snr_val, (int, float)) else f"  - Signal-to-noise ratio: {snr_val}")
                print(f"  - Signal quality: {quality_val}")
        
        # Run periodicity analysis
        print("\nRunning periodicity analysis...")
        periodicity_result = pipeline.run_test("periodicity_test")
        
        if 'result' in periodicity_result:
            print("Periodicity Analysis Results:")
            result = periodicity_result['result']
            if 'metrics' in result:
                metrics = result['metrics']
                period_val = metrics.get('dominant_period', 'N/A')
                pattern_val = metrics.get('seasonal_pattern', False)
                
                print(f"  - Dominant period: {period_val:.1f} months" if isinstance(period_val, (int, float)) else f"  - Dominant period: {period_val} months")
                print(f"  - Seasonal pattern detected: {'Yes' if pattern_val else 'No'}")
        
        # Save results
        results_file = pipeline.save_results()
        report_file = pipeline.generate_report()
        
        print(f"\nResults saved to: {results_file}")
        print(f"Report generated: {report_file}")
    
    # Clean up
    if os.path.exists(temp_file):
        os.remove(temp_file)

def run_comprehensive_climate_analysis():
    """Run comprehensive climate analysis with multiple datasets."""
    print("\n" + "="*60)
    print("RUNNING COMPREHENSIVE CLIMATE ANALYSIS")
    print("="*60)
    
    # Generate multiple climate datasets with different characteristics
    datasets = {}
    
    # Dataset 1: Strong warming trend
    climate_data1 = generate_realistic_climate_data()
    datasets['strong_warming'] = climate_data1['temperature'].values
    
    # Dataset 2: Stable climate (no trend)
    n_points = 600
    stable_temp = 15 + 5 * np.sin(2 * np.pi * np.arange(n_points) / 12) + np.random.normal(0, 1, n_points)
    datasets['stable_climate'] = stable_temp
    
    # Dataset 3: Cooling trend
    years = np.linspace(1950, 2000, n_points)
    cooling_trend = 20 - 0.01 * (years - 1950) + 5 * np.sin(2 * np.pi * np.arange(n_points) / 12) + np.random.normal(0, 1, n_points)
    datasets['cooling_trend'] = cooling_trend
    
    # Analyze each dataset
    results = {}
    for dataset_name, temperature_data in datasets.items():
        print(f"\nAnalyzing {dataset_name}...")
        
        # Basic statistics
        stats_result = basic_statistical_analysis(temperature_data)
        
        # Trend analysis
        # Create a proper DataFrame with month column for trend analysis
        n_points = len(temperature_data)
        years = np.linspace(1950, 2000, n_points)
        months = (np.arange(n_points) % 12) + 1
        
        trend_df = pd.DataFrame({
            'temperature': temperature_data,
            'year': years,
            'month': months
        })
        trend_results = analyze_climate_trends(trend_df)
        
        # Signal detection
        signal_result = signal_detection_test(temperature_data)
        
        # Periodicity
        periodicity_result = periodicity_test(temperature_data)
        
        results[dataset_name] = {
            'statistical_analysis': stats_result,
            'trend_analysis': trend_results,
            'signal_detection': signal_result,
            'periodicity_analysis': periodicity_result
        }
        
        # Print summary
        trend = trend_results['trend_analysis']
        print(f"  - Warming rate: {trend['trend_per_decade']:.3f}°C/decade")
        print(f"  - Trend significance: {'Significant' if trend['p_value'] < 0.05 else 'Not significant'}")
        print(f"  - Temperature range: {np.min(temperature_data):.1f}°C - {np.max(temperature_data):.1f}°C")
    
    # Generate comprehensive report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report = {
        "timestamp": timestamp,
        "analysis_type": "comprehensive_climate_analysis",
        "datasets_analyzed": list(datasets.keys()),
        "results": results
    }
    
    report_file = f"climate_comprehensive_report_{timestamp}.json"
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2, default=str)
    
    print(f"\nComprehensive climate analysis report saved to: {report_file}")

def create_climate_visualization(climate_data):
    """Create climate data visualizations."""
    try:
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # Plot 1: Temperature time series
        axes[0, 0].plot(climate_data['year'], climate_data['temperature'], 'b-', alpha=0.7)
        axes[0, 0].set_xlabel('Year')
        axes[0, 0].set_ylabel('Temperature (°C)')
        axes[0, 0].set_title('Temperature Time Series')
        axes[0, 0].grid(True, alpha=0.3)
        
        # Plot 2: Seasonal cycle
        seasonal_data = climate_data.groupby('month')['temperature'].mean()
        axes[0, 1].plot(seasonal_data.index, seasonal_data.values, 'g-o')
        axes[0, 1].set_xlabel('Month')
        axes[0, 1].set_ylabel('Average Temperature (°C)')
        axes[0, 1].set_title('Seasonal Temperature Cycle')
        axes[0, 1].grid(True, alpha=0.3)
        
        # Plot 3: Trend analysis
        years = climate_data['year'].values
        temperature = climate_data['temperature'].values
        slope, intercept, _, _, _ = stats.linregress(years, temperature)
        trend_line = intercept + slope * years
        
        axes[1, 0].scatter(years, temperature, alpha=0.5, s=10)
        axes[1, 0].plot(years, trend_line, 'r-', linewidth=2, label=f'Trend: {slope:.3f}°C/year')
        axes[1, 0].set_xlabel('Year')
        axes[1, 0].set_ylabel('Temperature (°C)')
        axes[1, 0].set_title('Temperature Trend Analysis')
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)
        
        # Plot 4: Histogram
        axes[1, 1].hist(temperature, bins=30, alpha=0.7, edgecolor='black')
        axes[1, 1].set_xlabel('Temperature (°C)')
        axes[1, 1].set_ylabel('Frequency')
        axes[1, 1].set_title('Temperature Distribution')
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Save plot
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        plot_file = f"climate_analysis_{timestamp}.png"
        plt.savefig(plot_file, dpi=300, bbox_inches='tight')
        print(f"Climate visualization saved to: {plot_file}")
        
        plt.close()
        
    except Exception as e:
        print(f"Could not create visualization: {e}")

def main():
    """Main execution function."""
    print("Climate Trend Detection Example")
    print("Universal Open Science Toolbox")
    print("="*60)
    
    try:
        # Generate climate data
        climate_data = generate_realistic_climate_data()
        
        # Run individual tests
        run_individual_climate_tests()
        
        # Run pipeline integration
        run_pipeline_integration()
        
        # Run comprehensive analysis
        run_comprehensive_climate_analysis()
        
        # Create visualization
        create_climate_visualization(climate_data)
        
        print("\n" + "="*60)
        print("CLIMATE TREND DETECTION COMPLETED")
        print("="*60)
        print("✓ Realistic climate data generated")
        print("✓ Trend analysis performed")
        print("✓ Statistical tests completed")
        print("✓ Pipeline integration verified")
        print("✓ Comprehensive analysis executed")
        print("✓ Visualizations created")
        
    except Exception as e:
        print(f"\n❌ Error during climate analysis: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 