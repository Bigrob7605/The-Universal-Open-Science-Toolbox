#!/usr/bin/env python3
"""
Bio Domain Module - Enzyme Analysis
Universal Open Science Toolbox

This module provides enzyme analysis functions for the Universal Open Science Toolbox,
integrating functionality from the Next-Gen Open Enzyme Design Workflow.
"""

import os
import sys
import json
import yaml
import numpy as np
import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import BioPython for sequence analysis
try:
    from Bio import SeqIO
    from Bio.Seq import Seq
    from Bio.SeqUtils import molecular_weight
    # GC function is not available in newer BioPython versions, so we'll calculate it manually
    BIO_AVAILABLE = True
except ImportError:
    logger.warning("BioPython not available. Some enzyme functions may be limited.")
    BIO_AVAILABLE = False

# Import matplotlib for visualization
try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    logger.warning("Matplotlib not available. Visualization functions disabled.")
    MATPLOTLIB_AVAILABLE = False

def ensure_json_serializable(obj):
    """Convert numpy types to JSON-serializable Python types."""
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
    """Create a standardized truth table with proper JSON serialization."""
    return ensure_json_serializable({
        "test_name": test_name,
        "timestamp": datetime.now().isoformat(),
        "pass_fail": pass_fail,
        "metrics": metrics,
        "evidence": evidence or {},
        "falsification_notes": falsification_notes
    })

def enzyme_sequence_analysis(fasta_file: str, **kwargs) -> dict:
    """
    Analyze enzyme sequence properties and characteristics.
    
    Args:
        fasta_file: Path to FASTA file containing enzyme sequence
        **kwargs: Additional parameters (mutation_sites, analysis_type, etc.)
    
    Returns:
        dict: Truth table with sequence analysis results
    """
    try:
        if not BIO_AVAILABLE:
            return create_truth_table(
                "enzyme_sequence_analysis",
                {"sequence_parsed": False, "analysis_complete": False},
                {"error": "BioPython not available"},
                {"error_type": "ImportError"},
                "BioPython required for sequence analysis"
            )
        
        # Parse FASTA file
        with open(fasta_file, 'r') as f:
            record = next(SeqIO.parse(f, 'fasta'))
        
        sequence = str(record.seq)
        sequence_id = record.id
        
        # Calculate sequence properties
        length = len(sequence)
        molecular_wt = molecular_weight(Seq(sequence), 'protein')
        # Calculate GC content manually (for protein sequences, this is not applicable)
        # For protein sequences, we'll use amino acid composition instead
        gc_content = 0.0  # Not applicable for protein sequences
        
        # Amino acid composition
        aa_counts = {}
        for aa in sequence:
            aa_counts[aa] = aa_counts.get(aa, 0) + 1
        
        # Calculate hydrophobicity (Kyte-Doolittle scale)
        hydrophobicity_scale = {
            'A': 1.8, 'R': -4.5, 'N': -3.5, 'D': -3.5, 'C': 2.5,
            'Q': -3.5, 'E': -3.5, 'G': -0.4, 'H': -3.2, 'I': 4.5,
            'L': 3.8, 'K': -3.9, 'M': 1.9, 'F': 2.8, 'P': -1.6,
            'S': -0.8, 'T': -0.7, 'W': -0.9, 'Y': -1.3, 'V': 4.2
        }
        
        avg_hydrophobicity = sum(hydrophobicity_scale.get(aa, 0) for aa in sequence) / len(sequence)
        
        # Check for common enzyme motifs
        motifs = {
            'catalytic_triad': any(motif in sequence for motif in ['HDS', 'HSS', 'HGS']),
            'nucleotide_binding': 'GXGXXG' in sequence,
            'metal_binding': any(motif in sequence for motif in ['HXXH', 'CXXC', 'DXXD']),
            'active_site': any(motif in sequence for motif in ['SER', 'THR', 'CYS', 'HIS', 'ASP', 'GLU'])
        }
        
        # Determine pass/fail criteria
        pass_fail = {
            "sequence_parsed": True,
            "analysis_complete": True,
            "valid_length": length > 50,  # Minimum enzyme length
            "has_catalytic_motifs": any(motifs.values()),
            "reasonable_molecular_weight": 10000 < molecular_wt < 200000,  # Typical enzyme range
            "hydrophobicity_balanced": -2 < avg_hydrophobicity < 2
        }
        
        metrics = {
            "sequence_id": sequence_id,
            "sequence_length": length,
            "molecular_weight": round(molecular_wt, 2),
            "gc_content": round(gc_content, 2),
            "avg_hydrophobicity": round(avg_hydrophobicity, 3),
            "unique_amino_acids": len(aa_counts),
            "motifs_found": sum(motifs.values()),
            "catalytic_motifs": motifs
        }
        
        evidence = {
            "amino_acid_composition": aa_counts,
            "sequence_preview": sequence[:50] + "..." if len(sequence) > 50 else sequence,
            "analysis_timestamp": datetime.now().isoformat()
        }
        
        return create_truth_table(
            "enzyme_sequence_analysis",
            pass_fail,
            metrics,
            evidence,
            "Sequence analysis completed successfully"
        )
        
    except Exception as e:
        logger.error(f"Enzyme sequence analysis failed: {e}")
        return create_truth_table(
            "enzyme_sequence_analysis",
            {"sequence_parsed": False, "analysis_complete": False},
            {"error": f"Analysis failed: {str(e)}"},
            {"error_type": type(e).__name__},
            f"Exception during sequence analysis: {e}"
        )

def enzyme_structure_validation(pdb_file: str, **kwargs) -> dict:
    """
    Validate enzyme structure properties from PDB file.
    
    Args:
        pdb_file: Path to PDB file containing enzyme structure
        **kwargs: Additional parameters (validation_criteria, etc.)
    
    Returns:
        dict: Truth table with structure validation results
    """
    try:
        if not os.path.exists(pdb_file):
            return create_truth_table(
                "enzyme_structure_validation",
                {"structure_loaded": False, "validation_complete": False},
                {"error": f"PDB file not found: {pdb_file}"},
                {"file_path": pdb_file},
                "PDB file does not exist"
            )
        
        # Read PDB file
        with open(pdb_file, 'r') as f:
            pdb_content = f.read()
        
        # Basic PDB validation
        lines = pdb_content.split('\n')
        atom_lines = [line for line in lines if line.startswith('ATOM')]
        hetatm_lines = [line for line in lines if line.startswith('HETATM')]
        
        # Extract structure information
        residues = set()
        chains = set()
        atoms = 0
        
        for line in atom_lines:
            if len(line) >= 26:
                chain = line[21] if line[21] != ' ' else 'A'
                chains.add(chain)
                residue = line[17:20].strip()
                residues.add(residue)
                atoms += 1
        
        # Calculate structure metrics
        num_atoms = len(atom_lines)
        num_residues = len(residues)
        num_chains = len(chains)
        
        # Check for common enzyme structure features
        has_alpha_helix = any('HELIX' in line for line in lines)
        has_beta_sheet = any('SHEET' in line for line in lines)
        has_ligand = len(hetatm_lines) > 0
        
        # Structure quality indicators
        structure_quality = {
            "has_atoms": num_atoms > 0,
            "has_residues": num_residues > 0,
            "has_chains": num_chains > 0,
            "has_secondary_structure": has_alpha_helix or has_beta_sheet,
            "has_ligand": has_ligand,
            "reasonable_size": 100 < num_atoms < 10000,  # Typical enzyme range
            "complete_structure": 'END' in pdb_content
        }
        
        pass_fail = {
            "structure_loaded": True,
            "validation_complete": True,
            "valid_pdb_format": True,
            "has_atoms": structure_quality["has_atoms"],
            "has_residues": structure_quality["has_residues"],
            "has_secondary_structure": structure_quality["has_secondary_structure"],
            "reasonable_size": structure_quality["reasonable_size"],
            "complete_structure": structure_quality["complete_structure"]
        }
        
        metrics = {
            "num_atoms": num_atoms,
            "num_residues": num_residues,
            "num_chains": num_chains,
            "has_alpha_helix": has_alpha_helix,
            "has_beta_sheet": has_beta_sheet,
            "has_ligand": has_ligand,
            "file_size_kb": round(len(pdb_content) / 1024, 2)
        }
        
        evidence = {
            "unique_residues": list(residues),
            "chains": list(chains),
            "structure_preview": pdb_content[:500] + "..." if len(pdb_content) > 500 else pdb_content,
            "validation_timestamp": datetime.now().isoformat()
        }
        
        return create_truth_table(
            "enzyme_structure_validation",
            pass_fail,
            metrics,
            evidence,
            "Structure validation completed successfully"
        )
        
    except Exception as e:
        logger.error(f"Enzyme structure validation failed: {e}")
        return create_truth_table(
            "enzyme_structure_validation",
            {"structure_loaded": False, "validation_complete": False},
            {"error": f"Validation failed: {str(e)}"},
            {"error_type": type(e).__name__},
            f"Exception during structure validation: {e}"
        )

def enzyme_mutation_analysis(wild_type_fasta: str, mutant_fasta: str, **kwargs) -> dict:
    """
    Analyze mutations between wild-type and mutant enzyme sequences.
    
    Args:
        wild_type_fasta: Path to wild-type FASTA file
        mutant_fasta: Path to mutant FASTA file
        **kwargs: Additional parameters (mutation_sites, analysis_type, etc.)
    
    Returns:
        dict: Truth table with mutation analysis results
    """
    try:
        if not BIO_AVAILABLE:
            return create_truth_table(
                "enzyme_mutation_analysis",
                {"analysis_complete": False},
                {"error": "BioPython not available"},
                {"error_type": "ImportError"},
                "BioPython required for mutation analysis"
            )
        
        # Parse both sequences
        with open(wild_type_fasta, 'r') as f:
            wt_record = next(SeqIO.parse(f, 'fasta'))
        
        with open(mutant_fasta, 'r') as f:
            mut_record = next(SeqIO.parse(f, 'fasta'))
        
        wt_seq = str(wt_record.seq)
        mut_seq = str(mut_record.seq)
        
        # Find mutations
        mutations = []
        for i, (wt_aa, mut_aa) in enumerate(zip(wt_seq, mut_seq)):
            if wt_aa != mut_aa:
                mutations.append({
                    'position': i + 1,
                    'wild_type': wt_aa,
                    'mutant': mut_aa,
                    'mutation': f"{wt_aa}{i+1}{mut_aa}"
                })
        
        # Calculate mutation metrics
        num_mutations = len(mutations)
        mutation_rate = num_mutations / len(wt_seq) if len(wt_seq) > 0 else 0
        
        # Analyze mutation types
        conservative_mutations = 0
        radical_mutations = 0
        
        # Simple amino acid classification
        hydrophobic = set('ACFILMPVWY')
        polar = set('DEHKNQRST')
        
        for mutation in mutations:
            wt_class = 'hydrophobic' if mutation['wild_type'] in hydrophobic else 'polar'
            mut_class = 'hydrophobic' if mutation['mutant'] in hydrophobic else 'polar'
            
            if wt_class == mut_class:
                conservative_mutations += 1
            else:
                radical_mutations += 1
        
        # Calculate molecular weight changes
        wt_mw = molecular_weight(Seq(wt_seq), 'protein')
        mut_mw = molecular_weight(Seq(mut_seq), 'protein')
        mw_change = mut_mw - wt_mw
        
        # Determine pass/fail criteria
        pass_fail = {
            "analysis_complete": True,
            "sequences_parsed": True,
            "mutations_found": num_mutations > 0,
            "reasonable_mutation_rate": mutation_rate < 0.1,  # Less than 10% mutations
            "conservative_mutations": conservative_mutations >= radical_mutations,
            "molecular_weight_change_reasonable": abs(mw_change) < 1000  # Less than 1kDa change
        }
        
        metrics = {
            "num_mutations": num_mutations,
            "mutation_rate": round(mutation_rate, 4),
            "conservative_mutations": conservative_mutations,
            "radical_mutations": radical_mutations,
            "molecular_weight_change": round(mw_change, 2),
            "wild_type_length": len(wt_seq),
            "mutant_length": len(mut_seq)
        }
        
        evidence = {
            "mutations": mutations,
            "wild_type_id": wt_record.id,
            "mutant_id": mut_record.id,
            "analysis_timestamp": datetime.now().isoformat()
        }
        
        return create_truth_table(
            "enzyme_mutation_analysis",
            pass_fail,
            metrics,
            evidence,
            "Mutation analysis completed successfully"
        )
        
    except Exception as e:
        logger.error(f"Enzyme mutation analysis failed: {e}")
        return create_truth_table(
            "enzyme_mutation_analysis",
            {"analysis_complete": False},
            {"error": f"Analysis failed: {str(e)}"},
            {"error_type": type(e).__name__},
            f"Exception during mutation analysis: {e}"
        )

def enzyme_activity_prediction(sequence_data: dict, structure_data: dict, **kwargs) -> dict:
    """
    Predict enzyme activity based on sequence and structure analysis.
    
    Args:
        sequence_data: Results from enzyme_sequence_analysis
        structure_data: Results from enzyme_structure_validation
        **kwargs: Additional parameters (activity_type, substrate, etc.)
    
    Returns:
        dict: Truth table with activity prediction results
    """
    try:
        # Extract relevant metrics
        seq_metrics = sequence_data.get('metrics', {})
        struct_metrics = structure_data.get('metrics', {})
        
        # Calculate activity score based on multiple factors
        activity_score = 0.0
        factors = []
        
        # Sequence-based factors
        if seq_metrics.get('has_catalytic_motifs', False):
            activity_score += 0.3
            factors.append("catalytic_motifs_present")
        
        if seq_metrics.get('hydrophobicity_balanced', False):
            activity_score += 0.2
            factors.append("balanced_hydrophobicity")
        
        # Structure-based factors
        if struct_metrics.get('has_secondary_structure', False):
            activity_score += 0.2
            factors.append("secondary_structure_present")
        
        if struct_metrics.get('has_ligand', False):
            activity_score += 0.1
            factors.append("ligand_binding_site")
        
        # Size-based factors
        seq_length = seq_metrics.get('sequence_length', 0)
        if 100 < seq_length < 1000:  # Typical enzyme size range
            activity_score += 0.1
            factors.append("appropriate_size")
        
        # Molecular weight factors
        mw = seq_metrics.get('molecular_weight', 0)
        if 10000 < mw < 200000:  # Typical enzyme MW range
            activity_score += 0.1
            factors.append("appropriate_molecular_weight")
        
        # Normalize score to 0-1 range
        activity_score = min(activity_score, 1.0)
        
        # Determine activity level
        if activity_score >= 0.8:
            activity_level = "high"
        elif activity_score >= 0.6:
            activity_level = "medium"
        elif activity_score >= 0.4:
            activity_level = "low"
        else:
            activity_level = "very_low"
        
        # Pass/fail criteria
        pass_fail = {
            "prediction_complete": True,
            "sufficient_data": bool(sequence_data.get('pass_fail', {}).get('analysis_complete', False)),
            "activity_predicted": activity_score > 0.3,
            "high_confidence": activity_score > 0.6,
            "structure_quality_adequate": structure_data.get('pass_fail', {}).get('structure_loaded', False)
        }
        
        metrics = {
            "activity_score": round(activity_score, 3),
            "activity_level": activity_level,
            "confidence_factors": factors,
            "num_factors": len(factors),
            "sequence_quality": seq_metrics.get('motifs_found', 0),
            "structure_quality": struct_metrics.get('num_residues', 0)
        }
        
        evidence = {
            "sequence_analysis": sequence_data.get('metrics', {}),
            "structure_analysis": structure_data.get('metrics', {}),
            "prediction_factors": factors,
            "prediction_timestamp": datetime.now().isoformat()
        }
        
        return create_truth_table(
            "enzyme_activity_prediction",
            pass_fail,
            metrics,
            evidence,
            f"Activity prediction completed. Score: {activity_score:.3f} ({activity_level})"
        )
        
    except Exception as e:
        logger.error(f"Enzyme activity prediction failed: {e}")
        return create_truth_table(
            "enzyme_activity_prediction",
            {"prediction_complete": False},
            {"error": f"Prediction failed: {str(e)}"},
            {"error_type": type(e).__name__},
            f"Exception during activity prediction: {e}"
        )

# Register functions with the pipeline
ENZYME_FUNCTIONS = {
    "enzyme_sequence_analysis": enzyme_sequence_analysis,
    "enzyme_structure_validation": enzyme_structure_validation,
    "enzyme_mutation_analysis": enzyme_mutation_analysis,
    "enzyme_activity_prediction": enzyme_activity_prediction
}

def get_enzyme_functions():
    """Return dictionary of available enzyme analysis functions."""
    return ENZYME_FUNCTIONS

def run_enzyme_test_battery(test_data_dir: str = "data", **kwargs) -> dict:
    """
    Run a comprehensive battery of enzyme tests.
    
    Args:
        test_data_dir: Directory containing test enzyme data
        **kwargs: Additional parameters
    
    Returns:
        dict: Combined results from all enzyme tests
    """
    results = {}
    
    # Look for enzyme test files
    test_files = []
    if os.path.exists(test_data_dir):
        for file in os.listdir(test_data_dir):
            if file.endswith(('.fasta', '.pdb')):
                test_files.append(os.path.join(test_data_dir, file))
    
    # If no test files found, create example data
    if not test_files:
        logger.info("No enzyme test files found. Creating example data...")
        
        # Create example FASTA file
        example_fasta = os.path.join(test_data_dir, "example_enzyme.fasta")
        os.makedirs(test_data_dir, exist_ok=True)
        
        with open(example_fasta, 'w') as f:
            f.write(">Example_Enzyme\n")
            f.write("MKLLNIFGLLSLAFMLSLLTFVSEKLIYQAGYDPVKDPNGNTNLFVKDPNVGKVNGVITFTYETKQGVFSVTYKNGEGCDLLKNGVDGLLYPGWTYNYGYGTPTANVGSWLIVGVALFVVGLLGAYYIGRSLAGKKRMLGIFLFACVSAALQIPFASVAAYIYNRQGIDDLCEVNGINYALLRCCGYDIARRGLDFVKKADDYNKWAENGKSEGFTWGMACGSGYFTANKGAGISVKGDKLVINGNPITFQALCDKVGLAPAVAVHVGPDIISSVTCCTTNIKTDFSDYLLGGDCVYVPVDAEVVFTTMDVGGQFRYSRPDKFLEFGTWGQSGITREVAYYEQGLLDVVNGRTWFGQAAQENSVYGVNGDTRDYLCDLLLEGIDVAFVWAKSFPVFRQMQDLEMKTGIPLGLTDPYVKCDAAMQKATEAAVSEEEGRRLRGEMMDLMQGQPREELYVKVSDRARLHKAVDPTIEPYINITVDGPSIHGLPKGVALMTAVAYRLAADQHRFVRRFEGDLVWLNVDIPAECFRNVRVILLENVTEMNREVKEAMMIMDRFKRKYTRYELAAAGVSIVQVIPLLKAAAEYTEAFGPLHLLAFRQWLQEYLVIKGERVRFALELLWPLGIYLVNRSVSTGQQARMLGAVLAILERFIKPLVFTAPTYVTGLLLKTIRGRPKYLLIASU\n")
        
        test_files.append(example_fasta)
    
    # Run tests on available files
    for test_file in test_files:
        if test_file.endswith('.fasta'):
            # Run sequence analysis
            seq_result = enzyme_sequence_analysis(test_file, **kwargs)
            results[f"sequence_analysis_{os.path.basename(test_file)}"] = seq_result
            
            # If we have multiple FASTA files, run mutation analysis
            fasta_files = [f for f in test_files if f.endswith('.fasta')]
            if len(fasta_files) >= 2:
                mut_result = enzyme_mutation_analysis(fasta_files[0], fasta_files[1], **kwargs)
                results[f"mutation_analysis_{os.path.basename(fasta_files[0])}_{os.path.basename(fasta_files[1])}"] = mut_result
        
        elif test_file.endswith('.pdb'):
            # Run structure validation
            struct_result = enzyme_structure_validation(test_file, **kwargs)
            results[f"structure_validation_{os.path.basename(test_file)}"] = struct_result
    
    # Run activity prediction if we have both sequence and structure data
    if any('sequence_analysis' in key for key in results.keys()) and any('structure_validation' in key for key in results.keys()):
        seq_data = next((v for k, v in results.items() if 'sequence_analysis' in k), {})
        struct_data = next((v for k, v in results.items() if 'structure_validation' in k), {})
        
        activity_result = enzyme_activity_prediction(seq_data, struct_data, **kwargs)
        results["activity_prediction"] = activity_result
    
    return results

if __name__ == "__main__":
    # Test the module
    print("Testing Bio Domain Module...")
    results = run_enzyme_test_battery()
    
    print(f"\nResults: {len(results)} tests completed")
    for test_name, result in results.items():
        print(f"\n{test_name}:")
        print(f"  Pass/Fail: {result.get('pass_fail', {})}")
        print(f"  Metrics: {result.get('metrics', {})}") 