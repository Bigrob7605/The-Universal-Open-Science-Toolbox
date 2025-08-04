#!/usr/bin/env python3
"""
Test Enzyme Functions
Universal Open Science Toolbox

Tests for the enzyme analysis functions from the bio domain module.
"""

import pytest
import numpy as np
import os
import tempfile
from pathlib import Path

# Import enzyme functions
from domain.bio import (
    enzyme_sequence_analysis,
    enzyme_structure_validation,
    enzyme_mutation_analysis,
    enzyme_activity_prediction,
    get_enzyme_functions
)

def create_test_fasta_file(content, filename):
    """Create a temporary FASTA file for testing."""
    with open(filename, 'w') as f:
        f.write(content)
    return filename

def create_test_pdb_file(content, filename):
    """Create a temporary PDB file for testing."""
    with open(filename, 'w') as f:
        f.write(content)
    return filename

def test_enzyme_functions_available():
    """Test that enzyme functions are available."""
    functions = get_enzyme_functions()
    
    assert isinstance(functions, dict)
    assert len(functions) > 0
    
    expected_functions = [
        "enzyme_sequence_analysis",
        "enzyme_structure_validation", 
        "enzyme_mutation_analysis",
        "enzyme_activity_prediction"
    ]
    
    for func_name in expected_functions:
        assert func_name in functions
        assert callable(functions[func_name])

def test_enzyme_sequence_analysis():
    """Test enzyme sequence analysis function."""
    # Create test FASTA file
    fasta_content = """>Test_Enzyme
MKLLNIFGLLSLAFMLSLLTFVSEKLIYQAGYDPVKDPNGNTNLFVKDPNVGKVNGVITFTYETKQGVFSVTYKNGEGCDLLKNGVDGLLYPGWTYNYGYGTPTANVGSWLIVGVALFVVGLLGAYYIGRSLAGKKRMLGIFLFACVSAALQIPFASVAAYIYNRQGIDDLCEVNGINYALLRCCGYDIARRGLDFVKKADDYNKWAENGKSEGFTWGMACGSGYFTANKGAGISVKGDKLVINGNPITFQALCDKVGLAPAVAVHVGPDIISSVTCCTTNIKTDFSDYLLGGDCVYVPVDAEVVFTTMDVGGQFRYSRPDKFLEFGTWGQSGITREVAYYEQGLLDVVNGRTWFGQAAQENSVYGVNGDTRDYLCDLLLEGIDVAFVWAKSFPVFRQMQDLEMKTGIPLGLTDPYVKCDAAMQKATEAAVSEEEGRRLRGEMMDLMQGQPREELYVKVSDRARLHKAVDPTIEPYINITVDGPSIHGLPKGVALMTAVAYRLAADQHRFVRRFEGDLVWLNVDIPAECFRNVRVILLENVTEMNREVKEAMMIMDRFKRKYTRYELAAAGVSIVQVIPLLKAAAEYTEAFGPLHLLAFRQWLQEYLVIKGERVRFALELLWPLGIYLVNRSVSTGQQARMLGAVLAILERFIKPLVFTAPTYVTGLLLKTIRGRPKYLLIASU"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.fasta', delete=False) as f:
        f.write(fasta_content)
        fasta_file = f.name
    
    try:
        result = enzyme_sequence_analysis(fasta_file)
        
        # Check truth table structure
        assert "test_name" in result
        assert "timestamp" in result
        assert "pass_fail" in result
        assert "metrics" in result
        assert "evidence" in result
        assert "falsification_notes" in result
        
        # Check specific results
        assert result["test_name"] == "enzyme_sequence_analysis"
        assert isinstance(result["pass_fail"], dict)
        assert isinstance(result["metrics"], dict)
        
        # Check that sequence was parsed successfully
        assert result["pass_fail"]["sequence_parsed"] == True
        assert result["pass_fail"]["analysis_complete"] == True
        
        # Check metrics
        metrics = result["metrics"]
        assert "sequence_id" in metrics
        assert "sequence_length" in metrics
        assert "molecular_weight" in metrics
        
    finally:
        os.unlink(fasta_file)

def test_enzyme_structure_validation():
    """Test enzyme structure validation function."""
    # Create test PDB file
    pdb_content = """REMARK  Test Enzyme Structure
TITLE     Test Enzyme Structure
COMPND    MOL_ID: 1;
COMPND   2 MOLECULE: Test Enzyme;
COMPND   3 CHAIN: A;
ATOM      1  N   ALA A   1      27.462  11.336  49.655  1.00 20.00           N  
ATOM      2  CA  ALA A   1      26.132  11.336  49.655  1.00 20.00           C  
ATOM      3  C   ALA A   1      25.132  11.336  49.655  1.00 20.00           C  
ATOM      4  O   ALA A   1      24.132  11.336  49.655  1.00 20.00           O  
HELIX    1   1 ALA A    1  ALA A    1  1                                   1
END"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.pdb', delete=False) as f:
        f.write(pdb_content)
        pdb_file = f.name
    
    try:
        result = enzyme_structure_validation(pdb_file)
        
        # Check truth table structure
        assert "test_name" in result
        assert "timestamp" in result
        assert "pass_fail" in result
        assert "metrics" in result
        assert "evidence" in result
        assert "falsification_notes" in result
        
        # Check specific results
        assert result["test_name"] == "enzyme_structure_validation"
        assert isinstance(result["pass_fail"], dict)
        assert isinstance(result["metrics"], dict)
        
        # Check that structure was loaded successfully
        assert result["pass_fail"]["structure_loaded"] == True
        assert result["pass_fail"]["validation_complete"] == True
        
        # Check metrics
        metrics = result["metrics"]
        assert "num_atoms" in metrics
        assert "num_residues" in metrics
        assert "num_chains" in metrics
        
    finally:
        os.unlink(pdb_file)

def test_enzyme_mutation_analysis():
    """Test enzyme mutation analysis function."""
    # Create test FASTA files
    wild_type_content = """>Wild_Type_Test
MKLLNIFGLLSLAFMLSLLTFVSEKLIYQAGYDPVKDPNGNTNLFVKDPNVGKVNGVITFTYETKQGVFSVTYKNGEGCDLLKNGVDGLLYPGWTYNYGYGTPTANVGSWLIVGVALFVVGLLGAYYIGRSLAGKKRMLGIFLFACVSAALQIPFASVAAYIYNRQGIDDLCEVNGINYALLRCCGYDIARRGLDFVKKADDYNKWAENGKSEGFTWGMACGSGYFTANKGAGISVKGDKLVINGNPITFQALCDKVGLAPAVAVHVGPDIISSVTCCTTNIKTDFSDYLLGGDCVYVPVDAEVVFTTMDVGGQFRYSRPDKFLEFGTWGQSGITREVAYYEQGLLDVVNGRTWFGQAAQENSVYGVNGDTRDYLCDLLLEGIDVAFVWAKSFPVFRQMQDLEMKTGIPLGLTDPYVKCDAAMQKATEAAVSEEEGRRLRGEMMDLMQGQPREELYVKVSDRARLHKAVDPTIEPYINITVDGPSIHGLPKGVALMTAVAYRLAADQHRFVRRFEGDLVWLNVDIPAECFRNVRVILLENVTEMNREVKEAMMIMDRFKRKYTRYELAAAGVSIVQVIPLLKAAAEYTEAFGPLHLLAFRQWLQEYLVIKGERVRFALELLWPLGIYLVNRSVSTGQQARMLGAVLAILERFIKPLVFTAPTYVTGLLLKTIRGRPKYLLIASU"""
    
    mutant_content = """>Mutant_Test
MKLLNIFGLLSLAFMLSLLTFVSEKLIYQAGYDPVKDPNGNTNLFVKDPNVGKVNGVITFTYETKQGVFSVTYKNGEGCDLLKNGVDGLLYPGWTYNYGYGTPTANVGSWLIVGVALFVVGLLGAYYIGRSLAGKKRMLGIFLFACVSAALQIPFASVAAYIYNRQGIDDLCEVNGINYALLRCCGYDIARRGLDFVKKADDYNKWAENGKSEGFTWGMACGSGYFTANKGAGISVKGDKLVINGNPITFQALCDKVGLAPAVAVHVGPDIISSVTCCTTNIKTDFSDYLLGGDCVYVPVDAEVVFTTMDVGGQFRYSRPDKFLEFGTWGQSGITREVAYYEQGLLDVVNGRTWFGQAAQENSVYGVNGDTRDYLCDLLLEGIDVAFVWAKSFPVFRQMQDLEMKTGIPLGLTDPYVKCDAAMQKATEAAVSEEEGRRLRGEMMDLMQGQPREELYVKVSDRARLHKAVDPTIEPYINITVDGPSIHGLPKGVALMTAVAYRLAADQHRFVRRFEGDLVWLNVDIPAECFRNVRVILLENVTEMNREVKEAMMIMDRFKRKYTRYELAAAGVSIVQVIPLLKAAAEYTEAFGPLHLLAFRQWLQEYLVIKGERVRFALELLWPLGIYLVNRSVSTGQQARMLGAVLAILERFIKPLVFTAPTYVTGLLLKTIRGRPKYLLIASU"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.fasta', delete=False) as f:
        f.write(wild_type_content)
        wild_type_file = f.name
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.fasta', delete=False) as f:
        f.write(mutant_content)
        mutant_file = f.name
    
    try:
        result = enzyme_mutation_analysis(wild_type_file, mutant_file)
        
        # Check truth table structure
        assert "test_name" in result
        assert "timestamp" in result
        assert "pass_fail" in result
        assert "metrics" in result
        assert "evidence" in result
        assert "falsification_notes" in result
        
        # Check specific results
        assert result["test_name"] == "enzyme_mutation_analysis"
        assert isinstance(result["pass_fail"], dict)
        assert isinstance(result["metrics"], dict)
        
        # Check that analysis was completed
        assert result["pass_fail"]["analysis_complete"] == True
        assert result["pass_fail"]["sequences_parsed"] == True
        
        # Check metrics
        metrics = result["metrics"]
        assert "num_mutations" in metrics
        assert "mutation_rate" in metrics
        assert "wild_type_length" in metrics
        assert "mutant_length" in metrics
        
    finally:
        os.unlink(wild_type_file)
        os.unlink(mutant_file)

def test_enzyme_activity_prediction():
    """Test enzyme activity prediction function."""
    # Create mock sequence and structure data
    sequence_data = {
        "pass_fail": {"analysis_complete": True},
        "metrics": {
            "sequence_length": 684,
            "molecular_weight": 75851.82,
            "has_catalytic_motifs": True,
            "hydrophobicity_balanced": True
        }
    }
    
    structure_data = {
        "pass_fail": {"structure_loaded": True},
        "metrics": {
            "num_residues": 684,
            "has_secondary_structure": True,
            "has_ligand": False
        }
    }
    
    result = enzyme_activity_prediction(sequence_data, structure_data)
    
    # Check truth table structure
    assert "test_name" in result
    assert "timestamp" in result
    assert "pass_fail" in result
    assert "metrics" in result
    assert "evidence" in result
    assert "falsification_notes" in result
    
    # Check specific results
    assert result["test_name"] == "enzyme_activity_prediction"
    assert isinstance(result["pass_fail"], dict)
    assert isinstance(result["metrics"], dict)
    
    # Check that prediction was completed
    assert result["pass_fail"]["prediction_complete"] == True
    
    # Check metrics
    metrics = result["metrics"]
    assert "activity_score" in metrics
    assert "activity_level" in metrics
    assert "confidence_factors" in metrics
    assert "num_factors" in metrics

def test_enzyme_functions_error_handling():
    """Test that enzyme functions handle errors gracefully."""
    # Test with non-existent file
    result = enzyme_sequence_analysis("non_existent_file.fasta")
    
    assert result["pass_fail"]["sequence_parsed"] == False
    assert result["pass_fail"]["analysis_complete"] == False
    assert "error" in result["metrics"]
    
    # Test with non-existent PDB file
    result = enzyme_structure_validation("non_existent_file.pdb")
    
    assert result["pass_fail"]["structure_loaded"] == False
    assert result["pass_fail"]["validation_complete"] == False
    assert "error" in result["metrics"]

def test_enzyme_functions_json_serializable():
    """Test that enzyme function results are JSON serializable."""
    import json
    
    # Create test data
    fasta_content = """>Test_Enzyme
MKLLNIFGLLSLAFMLSLLTFVSEKLIYQAGYDPVKDPNGNTNLFVKDPNVGKVNGVITFTYETKQGVFSVTYKNGEGCDLLKNGVDGLLYPGWTYNYGYGTPTANVGSWLIVGVALFVVGLLGAYYIGRSLAGKKRMLGIFLFACVSAALQIPFASVAAYIYNRQGIDDLCEVNGINYALLRCCGYDIARRGLDFVKKADDYNKWAENGKSEGFTWGMACGSGYFTANKGAGISVKGDKLVINGNPITFQALCDKVGLAPAVAVHVGPDIISSVTCCTTNIKTDFSDYLLGGDCVYVPVDAEVVFTTMDVGGQFRYSRPDKFLEFGTWGQSGITREVAYYEQGLLDVVNGRTWFGQAAQENSVYGVNGDTRDYLCDLLLEGIDVAFVWAKSFPVFRQMQDLEMKTGIPLGLTDPYVKCDAAMQKATEAAVSEEEGRRLRGEMMDLMQGQPREELYVKVSDRARLHKAVDPTIEPYINITVDGPSIHGLPKGVALMTAVAYRLAADQHRFVRRFEGDLVWLNVDIPAECFRNVRVILLENVTEMNREVKEAMMIMDRFKRKYTRYELAAAGVSIVQVIPLLKAAAEYTEAFGPLHLLAFRQWLQEYLVIKGERVRFALELLWPLGIYLVNRSVSTGQQARMLGAVLAILERFIKPLVFTAPTYVTGLLLKTIRGRPKYLLIASU"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.fasta', delete=False) as f:
        f.write(fasta_content)
        fasta_file = f.name
    
    try:
        result = enzyme_sequence_analysis(fasta_file)
        
        # Test JSON serialization
        json_str = json.dumps(result)
        assert isinstance(json_str, str)
        
        # Test that we can parse it back
        parsed_result = json.loads(json_str)
        assert isinstance(parsed_result, dict)
        assert "test_name" in parsed_result
        
    finally:
        os.unlink(fasta_file)

if __name__ == "__main__":
    pytest.main([__file__]) 