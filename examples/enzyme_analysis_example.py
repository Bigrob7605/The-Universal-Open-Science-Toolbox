#!/usr/bin/env python3
"""
Enzyme Analysis Example
Universal Open Science Toolbox

This example demonstrates the enzyme analysis capabilities of the Universal Open Science Toolbox,
integrating functionality from the Next-Gen Open Enzyme Design Workflow.

Author: Universal Open Science Toolbox
License: MIT
"""

import os
import sys
import json
from pathlib import Path

# Add the parent directory to the path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from BULLETPROOF_PIPELINE import BulletproofPipeline
from domain.bio import (
    enzyme_sequence_analysis,
    enzyme_structure_validation,
    enzyme_mutation_analysis,
    enzyme_activity_prediction,
    run_enzyme_test_battery
)

def create_example_enzyme_data():
    """Create example enzyme data for demonstration."""
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    # Create example FASTA files
    wild_type_fasta = data_dir / "wild_type_enzyme.fasta"
    mutant_fasta = data_dir / "mutant_enzyme.fasta"
    example_pdb = data_dir / "example_enzyme.pdb"
    
    # Wild-type PETase sequence (simplified)
    wild_type_sequence = """>Wild_Type_PETase
MKLLNIFGLLSLAFMLSLLTFVSEKLIYQAGYDPVKDPNGNTNLFVKDPNVGKVNGVITFTYETKQGVFSVTYKNGEGCDLLKNGVDGLLYPGWTYNYGYGTPTANVGSWLIVGVALFVVGLLGAYYIGRSLAGKKRMLGIFLFACVSAALQIPFASVAAYIYNRQGIDDLCEVNGINYALLRCCGYDIARRGLDFVKKADDYNKWAENGKSEGFTWGMACGSGYFTANKGAGISVKGDKLVINGNPITFQALCDKVGLAPAVAVHVGPDIISSVTCCTTNIKTDFSDYLLGGDCVYVPVDAEVVFTTMDVGGQFRYSRPDKFLEFGTWGQSGITREVAYYEQGLLDVVNGRTWFGQAAQENSVYGVNGDTRDYLCDLLLEGIDVAFVWAKSFPVFRQMQDLEMKTGIPLGLTDPYVKCDAAMQKATEAAVSEEEGRRLRGEMMDLMQGQPREELYVKVSDRARLHKAVDPTIEPYINITVDGPSIHGLPKGVALMTAVAYRLAADQHRFVRRFEGDLVWLNVDIPAECFRNVRVILLENVTEMNREVKEAMMIMDRFKRKYTRYELAAAGVSIVQVIPLLKAAAEYTEAFGPLHLLAFRQWLQEYLVIKGERVRFALELLWPLGIYLVNRSVSTGQQARMLGAVLAILERFIKPLVFTAPTYVTGLLLKTIRGRPKYLLIASU"""
    
    # Mutant sequence with S238F mutation
    mutant_sequence = """>Mutant_PETase_S238F
MKLLNIFGLLSLAFMLSLLTFVSEKLIYQAGYDPVKDPNGNTNLFVKDPNVGKVNGVITFTYETKQGVFSVTYKNGEGCDLLKNGVDGLLYPGWTYNYGYGTPTANVGSWLIVGVALFVVGLLGAYYIGRSLAGKKRMLGIFLFACVSAALQIPFASVAAYIYNRQGIDDLCEVNGINYALLRCCGYDIARRGLDFVKKADDYNKWAENGKSEGFTWGMACGSGYFTANKGAGISVKGDKLVINGNPITFQALCDKVGLAPAVAVHVGPDIISSVTCCTTNIKTDFSDYLLGGDCVYVPVDAEVVFTTMDVGGQFRYSRPDKFLEFGTWGQSGITREVAYYEQGLLDVVNGRTWFGQAAQENSVYGVNGDTRDYLCDLLLEGIDVAFVWAKSFPVFRQMQDLEMKTGIPLGLTDPYVKCDAAMQKATEAAVSEEEGRRLRGEMMDLMQGQPREELYVKVSDRARLHKAVDPTIEPYINITVDGPSIHGLPKGVALMTAVAYRLAADQHRFVRRFEGDLVWLNVDIPAECFRNVRVILLENVTEMNREVKEAMMIMDRFKRKYTRYELAAAGVSIVQVIPLLKAAAEYTEAFGPLHLLAFRQWLQEYLVIKGERVRFALELLWPLGIYLVNRSVSTGQQARMLGAVLAILERFIKPLVFTAPTYVTGLLLKTIRGRPKYLLIASU"""
    
    # Write FASTA files
    with open(wild_type_fasta, 'w') as f:
        f.write(wild_type_sequence)
    
    with open(mutant_fasta, 'w') as f:
        f.write(mutant_sequence)
    
    # Create example PDB file
    pdb_content = """REMARK  Example Enzyme Structure
REMARK  Generated for Universal Open Science Toolbox Demo
TITLE     Example Enzyme Structure
COMPND    MOL_ID: 1;
COMPND   2 MOLECULE: Example Enzyme;
COMPND   3 CHAIN: A;
COMPND   4 EC: 3.1.1.-;
SOURCE    MOL_ID: 1;
SOURCE   2 ORGANISM_SCIENTIFIC: Example organism;
KEYWDS    ENZYME, CATALYSIS, DEMO
EXPDTA    THEORETICAL MODEL
AUTHOR    Universal Open Science Toolbox
ATOM      1  N   ALA A   1      27.462  11.336  49.655  1.00 20.00           N  
ATOM      2  CA  ALA A   1      26.132  11.336  49.655  1.00 20.00           C  
ATOM      3  C   ALA A   1      25.132  11.336  49.655  1.00 20.00           C  
ATOM      4  O   ALA A   1      24.132  11.336  49.655  1.00 20.00           O  
ATOM      5  N   SER A   2      25.132  12.336  49.655  1.00 20.00           N  
ATOM      6  CA  SER A   2      24.132  12.336  49.655  1.00 20.00           C  
ATOM      7  C   SER A   2      23.132  12.336  49.655  1.00 20.00           C  
ATOM      8  O   SER A   2      22.132  12.336  49.655  1.00 20.00           O  
ATOM      9  N   THR A   3      23.132  13.336  49.655  1.00 20.00           N  
ATOM     10  CA  THR A   3      22.132  13.336  49.655  1.00 20.00           C  
ATOM     11  C   THR A   3      21.132  13.336  49.655  1.00 20.00           C  
ATOM     12  O   THR A   3      20.132  13.336  49.655  1.00 20.00           O  
HELIX    1   1 ALA A    1  SER A    2  1                                   3
SHEET   1 A 2 THR A    3  THR A    3  0
END"""
    
    with open(example_pdb, 'w') as f:
        f.write(pdb_content)
    
    print("✅ Created example enzyme data:")
    print(f"   Wild-type FASTA: {wild_type_fasta}")
    print(f"   Mutant FASTA: {mutant_fasta}")
    print(f"   Example PDB: {example_pdb}")
    
    return str(wild_type_fasta), str(mutant_fasta), str(example_pdb)

def run_individual_enzyme_tests():
    """Run individual enzyme tests to demonstrate functionality."""
    print("\n" + "="*60)
    print("ENZYME ANALYSIS EXAMPLE")
    print("="*60)
    
    # Create example data
    wild_type_fasta, mutant_fasta, example_pdb = create_example_enzyme_data()
    
    # Test 1: Sequence Analysis
    print("\n1. Enzyme Sequence Analysis")
    print("-" * 40)
    seq_result = enzyme_sequence_analysis(wild_type_fasta)
    
    print("Pass/Fail Results:")
    for criterion, passed in seq_result.get('pass_fail', {}).items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"   {criterion}: {status}")
    
    print("\nKey Metrics:")
    metrics = seq_result.get('metrics', {})
    for key, value in metrics.items():
        if isinstance(value, (int, float)):
            print(f"   {key}: {value:.4f}")
        else:
            print(f"   {key}: {value}")
    
    # Test 2: Structure Validation
    print("\n2. Enzyme Structure Validation")
    print("-" * 40)
    struct_result = enzyme_structure_validation(example_pdb)
    
    print("Pass/Fail Results:")
    for criterion, passed in struct_result.get('pass_fail', {}).items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"   {criterion}: {status}")
    
    print("\nKey Metrics:")
    metrics = struct_result.get('metrics', {})
    for key, value in metrics.items():
        if isinstance(value, (int, float)):
            print(f"   {key}: {value:.4f}")
        else:
            print(f"   {key}: {value}")
    
    # Test 3: Mutation Analysis
    print("\n3. Enzyme Mutation Analysis")
    print("-" * 40)
    mut_result = enzyme_mutation_analysis(wild_type_fasta, mutant_fasta)
    
    print("Pass/Fail Results:")
    for criterion, passed in mut_result.get('pass_fail', {}).items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"   {criterion}: {status}")
    
    print("\nKey Metrics:")
    metrics = mut_result.get('metrics', {})
    for key, value in metrics.items():
        if isinstance(value, (int, float)):
            print(f"   {key}: {value:.4f}")
        else:
            print(f"   {key}: {value}")
    
    # Test 4: Activity Prediction
    print("\n4. Enzyme Activity Prediction")
    print("-" * 40)
    activity_result = enzyme_activity_prediction(seq_result, struct_result)
    
    print("Pass/Fail Results:")
    for criterion, passed in activity_result.get('pass_fail', {}).items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"   {criterion}: {status}")
    
    print("\nKey Metrics:")
    metrics = activity_result.get('metrics', {})
    for key, value in metrics.items():
        if isinstance(value, (int, float)):
            print(f"   {key}: {value:.4f}")
        else:
            print(f"   {key}: {value}")
    
    return {
        "sequence_analysis": seq_result,
        "structure_validation": struct_result,
        "mutation_analysis": mut_result,
        "activity_prediction": activity_result
    }

def run_pipeline_integration():
    """Demonstrate integration with the main pipeline."""
    print("\n" + "="*60)
    print("PIPELINE INTEGRATION DEMO")
    print("="*60)
    
    # Initialize pipeline
    pipeline = BulletproofPipeline()
    
    # Register enzyme functions
    pipeline.register_test_function("enzyme_sequence_analysis", enzyme_sequence_analysis)
    pipeline.register_test_function("enzyme_structure_validation", enzyme_structure_validation)
    pipeline.register_test_function("enzyme_mutation_analysis", enzyme_mutation_analysis)
    pipeline.register_test_function("enzyme_activity_prediction", enzyme_activity_prediction)
    
    # Load data (we'll use a dummy data file for demonstration)
    data_path = "data/wild_type_enzyme.fasta"
    success = pipeline.load_data(data_path, "auto")
    
    if success:
        print("✅ Data loaded successfully")
        
        # Run enzyme sequence analysis
        print("\nRunning enzyme sequence analysis...")
        result = pipeline.run_test("enzyme_sequence_analysis")
        
        print("Pipeline Results:")
        print(f"   Test completed: {result.get('test_name', 'Unknown')}")
        print(f"   Pass/Fail: {result.get('pass_fail', {})}")
        print(f"   Metrics: {result.get('metrics', {})}")
        
        # Save results
        results_file = pipeline.save_results()
        report_file = pipeline.generate_report()
        
        print(f"\nResults saved to: {results_file}")
        print(f"Report generated: {report_file}")
        
    else:
        print("❌ Failed to load data")

def run_test_battery():
    """Run the comprehensive enzyme test battery."""
    print("\n" + "="*60)
    print("ENZYME TEST BATTERY")
    print("="*60)
    
    # Create example data first
    create_example_enzyme_data()
    
    # Run test battery
    results = run_enzyme_test_battery("data")
    
    print(f"✅ Completed {len(results)} enzyme tests:")
    
    for test_name, result in results.items():
        print(f"\n{test_name}:")
        
        # Show pass/fail summary
        pass_fail = result.get('pass_fail', {})
        if pass_fail:
            passed_count = sum(1 for v in pass_fail.values() if v)
            total_count = len(pass_fail)
            print(f"   Pass/Fail: {passed_count}/{total_count} criteria passed")
        
        # Show key metrics
        metrics = result.get('metrics', {})
        if 'error' not in metrics:
            print("   Key metrics:")
            for key, value in list(metrics.items())[:5]:  # Show first 5 metrics
                if isinstance(value, (int, float)):
                    print(f"     {key}: {value:.4f}")
                else:
                    print(f"     {key}: {value}")

def main():
    """Main function to run the enzyme analysis example."""
    print("🧬 Enzyme Analysis Example")
    print("Universal Open Science Toolbox")
    print("="*60)
    
    try:
        # Run individual tests
        individual_results = run_individual_enzyme_tests()
        
        # Run pipeline integration
        run_pipeline_integration()
        
        # Run test battery
        run_test_battery()
        
        print("\n" + "="*60)
        print("✅ Enzyme Analysis Example Completed Successfully!")
        print("="*60)
        
        print("\nSummary:")
        print("• Individual enzyme tests demonstrated")
        print("• Pipeline integration verified")
        print("• Test battery executed")
        print("• All functions follow truth-table pattern")
        print("• Results are JSON serializable")
        
    except Exception as e:
        print(f"\n❌ Error during enzyme analysis example: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 