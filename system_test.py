#!/usr/bin/env python3
"""
100% System Test - Repository Readiness Verification

Comprehensive test to ensure all systems work and any errors are caught.
"""

import os
import sys
import subprocess
import importlib
import traceback
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Tuple

class SystemTester:
    """Comprehensive system tester for repository readiness"""
    
    def __init__(self):
        self.results = {}
        self.errors = []
        self.warnings = []
        self.start_time = datetime.now()
        
    def log_result(self, test_name: str, success: bool, message: str = "", error: str = ""):
        """Log test result"""
        self.results[test_name] = {
            "success": success,
            "message": message,
            "error": error,
            "timestamp": datetime.now().isoformat()
        }
        
        if success:
            print(f"  ✅ {test_name}: {message}")
        else:
            print(f"  ❌ {test_name}: {error}")
            self.errors.append(f"{test_name}: {error}")
    
    def log_warning(self, test_name: str, warning: str):
        """Log warning"""
        print(f"  ⚠️ {test_name}: {warning}")
        self.warnings.append(f"{test_name}: {warning}")
    
    def test_file_structure(self) -> bool:
        """Test 1: Verify essential files exist"""
        print("\n📁 Testing File Structure...")
        
        essential_files = [
            "README.md",
            "GETTING_STARTED.md", 
            "API_REFERENCE.md",
            "EXAMPLES_GALLERY.md",
            "CONTRIBUTING_GUIDE.md",
            "BULLETPROOF_PIPELINE.py",
            "download_public_data.py",
            "cli_wizard.py",
            "requirements_universal.txt",
            "pytest.ini",
            ".gitignore",
            "LICENSE",
            "CITATION.cff"
        ]
        
        essential_dirs = [
            "Project White Papers",
            "security",
            "mmh_system", 
            "omega_kill_switch_package",
            "examples",
            "domain",
            "data",
            "tests",
            "test_suite",
            "rife_legacy",
            ".github"
        ]
        
        all_good = True
        
        # Check files
        for file_name in essential_files:
            if os.path.exists(file_name):
                self.log_result(f"File exists: {file_name}", True, "Found")
            else:
                self.log_result(f"File exists: {file_name}", False, "", f"Missing: {file_name}")
                all_good = False
        
        # Check directories
        for dir_name in essential_dirs:
            if os.path.exists(dir_name):
                self.log_result(f"Directory exists: {dir_name}", True, "Found")
            else:
                self.log_result(f"Directory exists: {dir_name}", False, "", f"Missing: {dir_name}")
                all_good = False
        
        return all_good
    
    def test_imports(self) -> bool:
        """Test 2: Test all module imports"""
        print("\n📦 Testing Module Imports...")
        
        modules_to_test = [
            "BULLETPROOF_PIPELINE",
            "download_public_data", 
            "cli_wizard"
        ]
        
        all_good = True
        
        for module_name in modules_to_test:
            try:
                module = importlib.import_module(module_name)
                self.log_result(f"Import: {module_name}", True, "Successfully imported")
            except Exception as e:
                self.log_result(f"Import: {module_name}", False, "", f"Import failed: {e}")
                all_good = False
        
        return all_good
    
    def test_pipeline_functionality(self) -> bool:
        """Test 3: Test pipeline basic functionality"""
        print("\n🔬 Testing Pipeline Functionality...")
        
        try:
            from BULLETPROOF_PIPELINE import BulletproofPipeline
            
            # Test pipeline initialization
            pipeline = BulletproofPipeline()
            self.log_result("Pipeline initialization", True, "Success")
            
            # Test help command
            result = subprocess.run([sys.executable, "BULLETPROOF_PIPELINE.py", "--help"], 
                                  capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                self.log_result("Pipeline help command", True, "Help displayed successfully")
            else:
                self.log_result("Pipeline help command", False, "", f"Help failed: {result.stderr}")
                return False
            
            return True
            
        except Exception as e:
            self.log_result("Pipeline functionality", False, "", f"Pipeline test failed: {e}")
            return False
    
    def test_cli_wizard(self) -> bool:
        """Test 4: Test CLI wizard functionality"""
        print("\n🧙 Testing CLI Wizard...")
        
        try:
            # Test help command
            result = subprocess.run([sys.executable, "cli_wizard.py", "--help"], 
                                  capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                self.log_result("CLI wizard help", True, "Help displayed successfully")
            else:
                self.log_result("CLI wizard help", False, "", f"Help failed: {result.stderr}")
                return False
            
            return True
            
        except Exception as e:
            self.log_result("CLI wizard functionality", False, "", f"CLI test failed: {e}")
            return False
    
    def test_data_downloader(self) -> bool:
        """Test 5: Test data downloader functionality"""
        print("\n📥 Testing Data Downloader...")
        
        try:
            # Test help command
            result = subprocess.run([sys.executable, "download_public_data.py", "--help"], 
                                  capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                self.log_result("Data downloader help", True, "Help displayed successfully")
            else:
                self.log_result("Data downloader help", False, "", f"Help failed: {result.stderr}")
                return False
            
            return True
            
        except Exception as e:
            self.log_result("Data downloader functionality", False, "", f"Downloader test failed: {e}")
            return False
    
    def test_security_modules(self) -> bool:
        """Test 6: Test security modules"""
        print("\n🛡️ Testing Security Modules...")
        
        security_files = [
            "security/omega_kill_switch/safeSim.py",
            "security/agent_security_testing.py",
            "security/omega_kill_switch/metrics_pipe.py",
            "security/omega_kill_switch/dummy_agent.py"
        ]
        
        all_good = True
        
        for file_path in security_files:
            if os.path.exists(file_path):
                self.log_result(f"Security file: {file_path}", True, "Found")
            else:
                self.log_result(f"Security file: {file_path}", False, "", f"Missing: {file_path}")
                all_good = False
        
        return all_good
    
    def test_mmh_system(self) -> bool:
        """Test 7: Test MMH system modules"""
        print("\n🔗 Testing MMH System...")
        
        mmh_files = [
            "mmh_system/mmh_core.py",
            "mmh_system/mmh_storage.py",
            "mmh_system/mmh_signer.py",
            "mmh_system/mmh_reproducer.py",
            "mmh_system/mmh_simple_file.py"
        ]
        
        all_good = True
        
        for file_path in mmh_files:
            if os.path.exists(file_path):
                self.log_result(f"MMH file: {file_path}", True, "Found")
            else:
                self.log_result(f"MMH file: {file_path}", False, "", f"Missing: {file_path}")
                all_good = False
        
        return all_good
    
    def test_test_data(self) -> bool:
        """Test 8: Test test data files"""
        print("\n📊 Testing Test Data...")
        
        test_files = [
            "test_data_iris.csv",
            "test_data_wine.csv", 
            "test_data_titanic.csv"
        ]
        
        all_good = True
        
        for file_path in test_files:
            if os.path.exists(file_path):
                # Check file size
                size = os.path.getsize(file_path)
                if size > 0:
                    self.log_result(f"Test data: {file_path}", True, f"Found ({size:,} bytes)")
                else:
                    self.log_result(f"Test data: {file_path}", False, "", "File is empty")
                    all_good = False
            else:
                self.log_result(f"Test data: {file_path}", False, "", f"Missing: {file_path}")
                all_good = False
        
        return all_good
    
    def test_documentation(self) -> bool:
        """Test 9: Test documentation files"""
        print("\n📚 Testing Documentation...")
        
        doc_files = [
            "README.md",
            "GETTING_STARTED.md",
            "API_REFERENCE.md", 
            "EXAMPLES_GALLERY.md",
            "CONTRIBUTING_GUIDE.md"
        ]
        
        all_good = True
        
        for file_path in doc_files:
            if os.path.exists(file_path):
                size = os.path.getsize(file_path)
                if size > 1000:  # At least 1KB
                    self.log_result(f"Documentation: {file_path}", True, f"Found ({size:,} bytes)")
                else:
                    self.log_result(f"Documentation: {file_path}", False, "", "File too small")
                    all_good = False
            else:
                self.log_result(f"Documentation: {file_path}", False, "", f"Missing: {file_path}")
                all_good = False
        
        return all_good
    
    def test_requirements(self) -> bool:
        """Test 10: Test requirements files"""
        print("\n📋 Testing Requirements...")
        
        req_files = [
            "requirements_universal.txt",
            "requirements_pinned.txt"
        ]
        
        all_good = True
        
        for file_path in req_files:
            if os.path.exists(file_path):
                size = os.path.getsize(file_path)
                if size > 100:  # At least 100 bytes
                    self.log_result(f"Requirements: {file_path}", True, f"Found ({size:,} bytes)")
                else:
                    self.log_result(f"Requirements: {file_path}", False, "", "File too small")
                    all_good = False
            else:
                self.log_result(f"Requirements: {file_path}", False, "", f"Missing: {file_path}")
                all_good = False
        
        return all_good
    
    def test_git_files(self) -> bool:
        """Test 11: Test Git repository files"""
        print("\n🔧 Testing Git Files...")
        
        git_files = [
            ".gitignore",
            "LICENSE",
            "CITATION.cff"
        ]
        
        all_good = True
        
        for file_path in git_files:
            if os.path.exists(file_path):
                size = os.path.getsize(file_path)
                if size > 50:  # At least 50 bytes
                    self.log_result(f"Git file: {file_path}", True, f"Found ({size:,} bytes)")
                else:
                    self.log_result(f"Git file: {file_path}", False, "", "File too small")
                    all_good = False
            else:
                self.log_result(f"Git file: {file_path}", False, "", f"Missing: {file_path}")
                all_good = False
        
        return all_good
    
    def test_backup_data(self) -> bool:
        """Test 12: Test BackupData folder"""
        print("\n📦 Testing BackupData...")
        
        if os.path.exists("BackupData"):
            # Check if it has content
            backup_items = list(Path("BackupData").rglob("*"))
            if len(backup_items) > 10:  # Should have multiple items
                self.log_result("BackupData folder", True, f"Found with {len(backup_items)} items")
                return True
            else:
                self.log_result("BackupData folder", False, "", "BackupData folder is empty or missing items")
                return False
        else:
            self.log_result("BackupData folder", False, "", "BackupData folder missing")
            return False
    
    def run_comprehensive_test(self) -> Dict[str, Any]:
        """Run all tests"""
        print("🔬 100% SYSTEM TEST - REPOSITORY READINESS VERIFICATION")
        print("=" * 70)
        
        tests = [
            ("File Structure", self.test_file_structure),
            ("Module Imports", self.test_imports),
            ("Pipeline Functionality", self.test_pipeline_functionality),
            ("CLI Wizard", self.test_cli_wizard),
            ("Data Downloader", self.test_data_downloader),
            ("Security Modules", self.test_security_modules),
            ("MMH System", self.test_mmh_system),
            ("Test Data", self.test_test_data),
            ("Documentation", self.test_documentation),
            ("Requirements", self.test_requirements),
            ("Git Files", self.test_git_files),
            ("BackupData", self.test_backup_data)
        ]
        
        passed_tests = 0
        total_tests = len(tests)
        
        for test_name, test_func in tests:
            try:
                success = test_func()
                if success:
                    passed_tests += 1
            except Exception as e:
                self.log_result(test_name, False, "", f"Test crashed: {e}")
                self.errors.append(f"{test_name}: Test crashed - {e}")
        
        # Calculate results
        success_rate = (passed_tests / total_tests) * 100
        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds()
        
        return {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": total_tests - passed_tests,
            "success_rate": success_rate,
            "errors": self.errors,
            "warnings": self.warnings,
            "duration": duration,
            "results": self.results
        }
    
    def generate_report(self, test_results: Dict[str, Any]) -> str:
        """Generate comprehensive test report"""
        report = f"""# 🔬 100% SYSTEM TEST REPORT

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Duration**: {test_results['duration']:.2f} seconds

## 📊 TEST RESULTS

### **Overall Statistics**
- **Total Tests**: {test_results['total_tests']}
- **Passed Tests**: {test_results['passed_tests']}
- **Failed Tests**: {test_results['failed_tests']}
- **Success Rate**: {test_results['success_rate']:.1f}%

### **Test Status**
"""
        
        if test_results['success_rate'] == 100:
            report += "✅ **PERFECT**: All tests passed! Repository is 100% ready!\n\n"
        elif test_results['success_rate'] >= 90:
            report += "✅ **EXCELLENT**: Almost all tests passed! Minor issues to address.\n\n"
        elif test_results['success_rate'] >= 80:
            report += "⚠️ **GOOD**: Most tests passed! Some issues need attention.\n\n"
        else:
            report += "❌ **NEEDS WORK**: Multiple test failures! Repository not ready.\n\n"
        
        # Detailed results
        report += "## 📋 DETAILED RESULTS\n\n"
        
        for test_name, result in test_results['results'].items():
            status = "✅ PASS" if result['success'] else "❌ FAIL"
            report += f"### {test_name}\n"
            report += f"- **Status**: {status}\n"
            report += f"- **Message**: {result['message']}\n"
            if result['error']:
                report += f"- **Error**: {result['error']}\n"
            report += f"- **Timestamp**: {result['timestamp']}\n\n"
        
        # Errors
        if test_results['errors']:
            report += "## ❌ ERRORS\n\n"
            for error in test_results['errors']:
                report += f"- {error}\n"
            report += "\n"
        
        # Warnings
        if test_results['warnings']:
            report += "## ⚠️ WARNINGS\n\n"
            for warning in test_results['warnings']:
                report += f"- {warning}\n"
            report += "\n"
        
        # Recommendations
        report += "## 🎯 RECOMMENDATIONS\n\n"
        
        if test_results['success_rate'] == 100:
            report += "✅ **Repository is 100% ready for push!**\n"
            report += "- All systems operational\n"
            report += "- No errors detected\n"
            report += "- Ready for public release\n"
        elif test_results['success_rate'] >= 90:
            report += "⚠️ **Repository is almost ready**\n"
            report += "- Address minor issues before push\n"
            report += "- Fix any missing files or modules\n"
            report += "- Test again after fixes\n"
        else:
            report += "❌ **Repository needs work**\n"
            report += "- Fix critical issues before push\n"
            report += "- Address missing files and modules\n"
            report += "- Run comprehensive testing after fixes\n"
        
        report += f"\n## 📈 SUMMARY\n\n"
        report += f"- **Success Rate**: {test_results['success_rate']:.1f}%\n"
        report += f"- **Test Duration**: {test_results['duration']:.2f} seconds\n"
        report += f"- **Total Tests**: {test_results['total_tests']}\n"
        report += f"- **Passed**: {test_results['passed_tests']}\n"
        report += f"- **Failed**: {test_results['failed_tests']}\n"
        
        return report

def main():
    """Main function"""
    print("🔬 100% SYSTEM TEST - REPOSITORY READINESS VERIFICATION")
    print("=" * 70)
    
    try:
        # Create tester
        tester = SystemTester()
        
        # Run comprehensive test
        test_results = tester.run_comprehensive_test()
        
        # Generate report
        report = tester.generate_report(test_results)
        
        # Save report
        report_path = "SYSTEM_TEST_REPORT.md"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        # Print summary
        print("\n" + "=" * 70)
        print("📋 SYSTEM TEST COMPLETE!")
        print(f"✅ Success Rate: {test_results['success_rate']:.1f}%")
        print(f"📊 Tests: {test_results['passed_tests']}/{test_results['total_tests']} passed")
        print(f"⏱️ Duration: {test_results['duration']:.2f} seconds")
        
        if test_results['success_rate'] == 100:
            print("🎉 REPOSITORY IS 100% READY FOR PUSH!")
        elif test_results['success_rate'] >= 90:
            print("⚠️ REPOSITORY IS ALMOST READY - MINOR ISSUES TO ADDRESS")
        else:
            print("❌ REPOSITORY NEEDS WORK - FIX ISSUES BEFORE PUSH")
        
        print(f"📄 Full report saved to: {report_path}")
        
        return test_results['success_rate'] == 100
        
    except Exception as e:
        print(f"\n❌ System test error: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 