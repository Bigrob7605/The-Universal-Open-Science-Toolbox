#!/usr/bin/env python3
"""
Review White Project Folder MD Files

Systematically reviews all white paper files to ensure they're in sync,
contain no mistakes or fake data, and reflect all current progress.
"""

import os
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

def get_white_paper_files():
    """Get list of white paper files to review"""
    white_paper_files = [
        "Project White Papers/README.md",
        "Project White Papers/API_REFERENCE.md", 
        "Project White Papers/GETTING_STARTED.md",
        "Project White Papers/EXAMPLES_GALLERY.md",
        "Project White Papers/CONTRIBUTING_GUIDE.md",
        "Project White Papers/COMPLETION_STATUS.md",
        "Project White Papers/DOCUMENTATION_CONSOLIDATION_SUMMARY.md"
    ]
    return white_paper_files

def read_file_content(file_path: str) -> str:
    """Read file content safely"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading {file_path}: {e}"

def check_for_fake_data(content: str, file_name: str) -> List[str]:
    """Check for potential fake data or mistakes"""
    issues = []
    
    # Check for placeholder text
    placeholder_patterns = [
        r"your-repo",
        r"your-username", 
        r"your-data\.csv",
        r"example\.com",
        r"placeholder",
        r"TODO",
        r"FIXME",
        r"TBD"
    ]
    
    for pattern in placeholder_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        if matches:
            issues.append(f"Potential placeholder text found: {pattern} ({len(matches)} instances)")
    
    # Check for unrealistic claims
    unrealistic_patterns = [
        r"100% accuracy",
        r"perfect results",
        r"no errors",
        r"flawless",
        r"bulletproof.*without.*issues"
    ]
    
    for pattern in unrealistic_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        if matches:
            issues.append(f"Potentially unrealistic claim: {pattern} ({len(matches)} instances)")
    
    # Check for missing implementation details
    missing_patterns = [
        r"not implemented",
        r"coming soon",
        r"future version",
        r"planned feature"
    ]
    
    for pattern in missing_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        if matches:
            issues.append(f"Missing implementation noted: {pattern} ({len(matches)} instances)")
    
    return issues

def check_for_sync_issues(content: str, file_name: str) -> List[str]:
    """Check for synchronization issues between files"""
    issues = []
    
    # Check for inconsistent version numbers
    version_patterns = [
        r"v\d+\.\d+\.\d+",
        r"version \d+",
        r"release \d+"
    ]
    
    versions = []
    for pattern in version_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        versions.extend(matches)
    
    if len(set(versions)) > 1:
        issues.append(f"Inconsistent version numbers found: {set(versions)}")
    
    # Check for broken links or references
    broken_ref_patterns = [
        r"\[.*\]\(.*\)",  # Markdown links
        r"`[^`]+`",       # Code references
        r"import [a-zA-Z_][a-zA-Z0-9_]*"  # Import statements
    ]
    
    # Check for file references that might not exist
    file_refs = re.findall(r"`([^`]+\.(py|md|txt|json|csv))`", content)
    for file_ref in file_refs:
        if not os.path.exists(file_ref[0]):
            issues.append(f"Referenced file may not exist: {file_ref[0]}")
    
    return issues

def check_for_current_progress(content: str, file_name: str) -> List[str]:
    """Check if file reflects current project progress"""
    issues = []
    
    # Check for recent features
    recent_features = [
        "Omega Kill Switch",
        "MMH System", 
        "Kai Core",
        "immutable registry",
        "hero points",
        "bulletproof pipeline",
        "comprehensive test battery"
    ]
    
    missing_features = []
    for feature in recent_features:
        if feature.lower() not in content.lower():
            missing_features.append(feature)
    
    if missing_features:
        issues.append(f"Recent features not mentioned: {', '.join(missing_features)}")
    
    # Check for outdated information
    outdated_patterns = [
        r"RIFE.*theory.*alive",
        r"experimental.*phase",
        r"beta.*version",
        r"preliminary.*results"
    ]
    
    for pattern in outdated_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        if matches:
            issues.append(f"Potentially outdated information: {pattern}")
    
    return issues

def check_file_structure(content: str, file_name: str) -> List[str]:
    """Check file structure and formatting"""
    issues = []
    
    lines = content.split('\n')
    
    # Check for proper headers
    headers = [line for line in lines if line.startswith('#')]
    if len(headers) < 3:
        issues.append("Insufficient header structure (less than 3 headers)")
    
    # Check for code blocks
    code_blocks = re.findall(r'```[\s\S]*?```', content)
    if len(code_blocks) < 2:
        issues.append("Limited code examples (less than 2 code blocks)")
    
    # Check for proper markdown formatting
    if not re.search(r'\*\*.*\*\*', content):  # Bold text
        issues.append("No bold formatting found")
    
    if not re.search(r'\*.*\*', content):  # Italic text
        issues.append("No italic formatting found")
    
    return issues

def analyze_file(file_path: str) -> Dict[str, Any]:
    """Analyze a single file for issues"""
    print(f"🔍 Analyzing {file_path}...")
    
    content = read_file_content(file_path)
    file_size = len(content)
    
    analysis = {
        "file_path": file_path,
        "file_size": file_size,
        "lines": len(content.split('\n')),
        "fake_data_issues": check_for_fake_data(content, file_path),
        "sync_issues": check_for_sync_issues(content, file_path),
        "progress_issues": check_for_current_progress(content, file_path),
        "structure_issues": check_file_structure(content, file_path),
        "total_issues": 0
    }
    
    # Count total issues
    analysis["total_issues"] = (
        len(analysis["fake_data_issues"]) +
        len(analysis["sync_issues"]) +
        len(analysis["progress_issues"]) +
        len(analysis["structure_issues"])
    )
    
    return analysis

def generate_review_report(analyses: List[Dict[str, Any]]) -> str:
    """Generate comprehensive review report"""
    report = "# 📋 WHITE PROJECT FOLDER REVIEW REPORT\n\n"
    report += f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    # Summary statistics
    total_files = len(analyses)
    total_issues = sum(analysis["total_issues"] for analysis in analyses)
    total_size = sum(analysis["file_size"] for analysis in analyses)
    
    report += f"## 📊 SUMMARY\n\n"
    report += f"- **Files Reviewed**: {total_files}\n"
    report += f"- **Total Issues Found**: {total_issues}\n"
    report += f"- **Total Size**: {total_size:,} bytes\n"
    report += f"- **Average Issues per File**: {total_issues/total_files:.1f}\n\n"
    
    # File-by-file analysis
    report += f"## 📁 FILE ANALYSIS\n\n"
    
    for analysis in analyses:
        file_name = os.path.basename(analysis["file_path"])
        report += f"### {file_name}\n\n"
        report += f"- **Size**: {analysis['file_size']:,} bytes\n"
        report += f"- **Lines**: {analysis['lines']}\n"
        report += f"- **Issues**: {analysis['total_issues']}\n\n"
        
        if analysis["fake_data_issues"]:
            report += f"**Fake Data Issues:**\n"
            for issue in analysis["fake_data_issues"]:
                report += f"- {issue}\n"
            report += "\n"
        
        if analysis["sync_issues"]:
            report += f"**Sync Issues:**\n"
            for issue in analysis["sync_issues"]:
                report += f"- {issue}\n"
            report += "\n"
        
        if analysis["progress_issues"]:
            report += f"**Progress Issues:**\n"
            for issue in analysis["progress_issues"]:
                report += f"- {issue}\n"
            report += "\n"
        
        if analysis["structure_issues"]:
            report += f"**Structure Issues:**\n"
            for issue in analysis["structure_issues"]:
                report += f"- {issue}\n"
            report += "\n"
        
        if analysis["total_issues"] == 0:
            report += f"✅ **No issues found**\n\n"
    
    # Overall assessment
    report += f"## 🎯 OVERALL ASSESSMENT\n\n"
    
    if total_issues == 0:
        report += f"✅ **PERFECT**: All files are in sync, contain no mistakes or fake data, and reflect current progress!\n\n"
    elif total_issues < 5:
        report += f"✅ **GOOD**: Minor issues found, but overall quality is high.\n\n"
    elif total_issues < 10:
        report += f"⚠️ **ACCEPTABLE**: Some issues found that should be addressed.\n\n"
    else:
        report += f"❌ **NEEDS ATTENTION**: Multiple issues found that require immediate attention.\n\n"
    
    report += f"## 🔧 RECOMMENDATIONS\n\n"
    
    if total_issues > 0:
        report += f"1. **Address Critical Issues**: Fix any fake data or sync issues first\n"
        report += f"2. **Update Progress**: Ensure all recent features are mentioned\n"
        report += f"3. **Improve Structure**: Add proper headers and formatting\n"
        report += f"4. **Verify References**: Check that all file references exist\n"
    else:
        report += f"1. **Maintain Quality**: Continue current high standards\n"
        report += f"2. **Regular Reviews**: Schedule periodic reviews\n"
        report += f"3. **Update Progress**: Keep documentation current with new features\n"
    
    return report

def main():
    """Main function"""
    print("🔍 REVIEWING WHITE PROJECT FOLDER MD FILES")
    print("=" * 60)
    
    try:
        # Get files to review
        white_paper_files = get_white_paper_files()
        
        # Analyze each file
        analyses = []
        for file_path in white_paper_files:
            if os.path.exists(file_path):
                analysis = analyze_file(file_path)
                analyses.append(analysis)
                
                # Print quick summary
                status = "✅" if analysis["total_issues"] == 0 else "⚠️"
                print(f"  {status} {os.path.basename(file_path)}: {analysis['total_issues']} issues")
            else:
                print(f"  ❌ {file_path} (not found)")
        
        # Generate report
        report = generate_review_report(analyses)
        
        # Save report
        report_path = "WHITE_PAPERS_REVIEW_REPORT.md"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print("\n" + "=" * 60)
        print("📋 REVIEW COMPLETE!")
        
        total_issues = sum(analysis["total_issues"] for analysis in analyses)
        if total_issues == 0:
            print("✅ All files are in sync, contain no mistakes or fake data!")
            print("✅ All current progress is properly reflected!")
        else:
            print(f"⚠️ {total_issues} issues found - see {report_path} for details")
        
        print(f"📄 Full report saved to: {report_path}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Review error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 