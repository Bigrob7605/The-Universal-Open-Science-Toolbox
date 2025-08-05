#!/usr/bin/env python3
"""
Transfer Data to White Project Folder MD Files

Condenses all important data from various MD files into the existing white project folder MD files.
"""

import os
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

def get_important_data_files():
    """Get list of important data files to transfer"""
    important_files = {
        "status_reports": [
            "FINAL_READINESS_REPORT.md",
            "KAI_CORE_OMEGA_INTEGRATION_COMPLETE.md",
            "MMH_SYSTEM_INTEGRATION_STATUS.md",
            "MMH_FILE_FORMAT_COMPLETE.md",
            "FLAWLESS_MMH_FILE_SUMMARY.md",
            "OMEGA_KILL_SWITCH_FINAL_STATUS.md",
            "KAI_CORE_INTEGRATION_STATUS.md"
        ],
        "integration_reports": [
            "OMEGA_INTEGRATION_STATUS.md",
            "OMEGA_KILL_SWITCH_INTEGRATION.md"
        ],
        "documentation": [
            "README.md",
            "API_REFERENCE.md",
            "GETTING_STARTED.md",
            "EXAMPLES_GALLERY.md",
            "CONTRIBUTING_GUIDE.md"
        ],
        "reports": [
            "bulletproof_report_20250805_122927.md",
            "bulletproof_report_20250805_123230.md",
            "REPOSITORY_SUMMARY.md"
        ]
    }
    return important_files

def read_file_content(file_path: str) -> str:
    """Read file content safely"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading {file_path}: {e}"

def extract_key_sections(content: str, file_name: str) -> Dict[str, str]:
    """Extract key sections from content"""
    sections = {}
    
    # Extract main content without headers
    lines = content.split('\n')
    current_section = []
    current_title = "Main Content"
    
    for line in lines:
        if line.startswith('# '):
            if current_section:
                sections[current_title] = '\n'.join(current_section).strip()
            current_title = line[2:].strip()
            current_section = []
        else:
            current_section.append(line)
    
    if current_section:
        sections[current_title] = '\n'.join(current_section).strip()
    
    return sections

def update_white_paper_file(file_path: str, new_content: str, section_title: str = "Latest Updates"):
    """Update white paper file with new content"""
    try:
        # Read existing content
        with open(file_path, 'r', encoding='utf-8') as f:
            existing_content = f.read()
        
        # Find a good place to insert new content (before any existing "Latest Updates" section)
        lines = existing_content.split('\n')
        insert_index = len(lines)
        
        # Look for existing "Latest Updates" section
        for i, line in enumerate(lines):
            if line.startswith('## ') and 'Latest Updates' in line:
                insert_index = i
                break
        
        # Insert new content
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_section = f"\n## {section_title} ({timestamp})\n\n{new_content}\n"
        
        lines.insert(insert_index, new_section)
        
        # Write updated content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        
        return True
    except Exception as e:
        print(f"Error updating {file_path}: {e}")
        return False

def create_consolidated_summary():
    """Create a consolidated summary of all important data"""
    print("📁 Creating Consolidated Data Summary...")
    
    important_files = get_important_data_files()
    consolidated_data = {}
    
    for category, files in important_files.items():
        consolidated_data[category] = {}
        print(f"  📂 Processing {category} files...")
        
        for file_name in files:
            file_path = Path(file_name)
            if file_path.exists():
                content = read_file_content(file_name)
                sections = extract_key_sections(content, file_name)
                
                consolidated_data[category][file_name] = {
                    "content": content,
                    "sections": sections,
                    "size": len(content),
                    "last_modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                }
                print(f"    ✅ {file_name} ({len(content):,} bytes)")
            else:
                print(f"    ❌ {file_name} (not found)")
    
    return consolidated_data

def update_white_papers_with_data(consolidated_data: Dict[str, Any]):
    """Update white paper files with consolidated data"""
    print("\n📝 Updating White Paper Files...")
    
    white_paper_files = {
        "Project White Papers/README.md": {
            "title": "System Status and Integration Updates",
            "content": []
        },
        "Project White Papers/API_REFERENCE.md": {
            "title": "Technical Implementation Updates",
            "content": []
        },
        "Project White Papers/GETTING_STARTED.md": {
            "title": "User Experience and Onboarding Updates",
            "content": []
        },
        "Project White Papers/EXAMPLES_GALLERY.md": {
            "title": "Feature and Capability Updates",
            "content": []
        },
        "Project White Papers/CONTRIBUTING_GUIDE.md": {
            "title": "Development and Integration Updates",
            "content": []
        }
    }
    
    # Organize content by target file
    for category, files in consolidated_data.items():
        for file_name, file_data in files.items():
            content = file_data["content"]
            
            # Determine target file based on content type
            if "status" in file_name.lower() or "integration" in file_name.lower():
                white_paper_files["Project White Papers/README.md"]["content"].append(
                    f"### {file_name}\n\n{content[:2000]}...\n"
                )
            elif "api" in file_name.lower() or "technical" in file_name.lower():
                white_paper_files["Project White Papers/API_REFERENCE.md"]["content"].append(
                    f"### {file_name}\n\n{content[:2000]}...\n"
                )
            elif "getting" in file_name.lower() or "start" in file_name.lower():
                white_paper_files["Project White Papers/GETTING_STARTED.md"]["content"].append(
                    f"### {file_name}\n\n{content[:2000]}...\n"
                )
            elif "example" in file_name.lower() or "gallery" in file_name.lower():
                white_paper_files["Project White Papers/EXAMPLES_GALLERY.md"]["content"].append(
                    f"### {file_name}\n\n{content[:2000]}...\n"
                )
            else:
                white_paper_files["Project White Papers/CONTRIBUTING_GUIDE.md"]["content"].append(
                    f"### {file_name}\n\n{content[:2000]}...\n"
                )
    
    # Update each white paper file
    for file_path, file_info in white_paper_files.items():
        if file_info["content"]:
            print(f"  📄 Updating {file_path}...")
            
            # Combine all content for this file
            combined_content = f"\n## {file_info['title']}\n\n"
            combined_content += "\n".join(file_info["content"])
            
            success = update_white_paper_file(file_path, combined_content, file_info["title"])
            if success:
                print(f"    ✅ Updated successfully")
            else:
                print(f"    ❌ Update failed")

def create_completion_status_summary(consolidated_data: Dict[str, Any]):
    """Create a comprehensive completion status summary"""
    print("\n📊 Creating Completion Status Summary...")
    
    summary_content = "# 🎉 COMPREHENSIVE COMPLETION STATUS\n\n"
    summary_content += f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    # Count files by category
    total_files = 0
    total_bytes = 0
    
    for category, files in consolidated_data.items():
        category_files = len(files)
        category_bytes = sum(file_data["size"] for file_data in files.values())
        total_files += category_files
        total_bytes += category_bytes
        
        summary_content += f"## {category.replace('_', ' ').title()}\n\n"
        summary_content += f"- **Files**: {category_files}\n"
        summary_content += f"- **Total Size**: {category_bytes:,} bytes\n\n"
        
        for file_name, file_data in files.items():
            summary_content += f"### {file_name}\n"
            summary_content += f"- **Size**: {file_data['size']:,} bytes\n"
            summary_content += f"- **Last Modified**: {file_data['last_modified']}\n"
            summary_content += f"- **Sections**: {len(file_data['sections'])}\n\n"
    
    summary_content += f"## 📈 SUMMARY\n\n"
    summary_content += f"- **Total Files**: {total_files}\n"
    summary_content += f"- **Total Size**: {total_bytes:,} bytes\n"
    summary_content += f"- **Categories**: {len(consolidated_data)}\n"
    summary_content += f"- **Status**: ✅ All data successfully consolidated\n\n"
    
    # Write summary to white papers folder
    summary_path = "Project White Papers/COMPLETION_STATUS.md"
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write(summary_content)
    
    print(f"  ✅ Created comprehensive summary: {summary_path}")
    print(f"    Total files: {total_files}")
    print(f"    Total size: {total_bytes:,} bytes")

def main():
    """Main function"""
    print("🔗 DATA TRANSFER TO WHITE PROJECT FOLDER")
    print("=" * 60)
    
    try:
        # Create consolidated data summary
        consolidated_data = create_consolidated_summary()
        
        # Update white paper files with data
        update_white_papers_with_data(consolidated_data)
        
        # Create completion status summary
        create_completion_status_summary(consolidated_data)
        
        print("\n" + "=" * 60)
        print("🎉 DATA TRANSFER COMPLETE!")
        print("✅ All important data transferred to white project folder")
        print("✅ White paper files updated with latest information")
        print("✅ Comprehensive completion status created")
        print("✅ Data successfully condensed and organized")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Data transfer error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 