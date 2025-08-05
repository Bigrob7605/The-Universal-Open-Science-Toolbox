#!/usr/bin/env python3
"""
Test script for Omega Kill Switch integration.

This script demonstrates how the Omega Kill Switch protects against agents
that try to make absolute truth claims.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from security.agent_security_testing import AgentSecurityTester, SecurityMonitor
from security.omega_kill_switch import run_agent, EXIT_OK, EXIT_VIOLATION, EXIT_TIMEOUT

def test_benign_agent():
    """Test a benign agent that doesn't make forbidden claims."""
    print("🧪 Testing benign agent...")
    
    # Create a benign agent script
    benign_script = """
import sys
print("I am a benign agent doing normal analysis.")
print("The data shows interesting patterns.")
print("I have no absolute claims to make.")
sys.exit(0)
"""
    
    # Write to temporary file
    with open("temp_benign_agent.py", "w") as f:
        f.write(benign_script)
    
    # Test with Omega Kill Switch
    result = run_agent(["python", "temp_benign_agent.py"], timeout=10.0)
    
    print(f"Exit code: {result}")
    print(f"Status: {'✅ PASSED' if result == EXIT_OK else '❌ FAILED'}")
    
    # Cleanup
    os.remove("temp_benign_agent.py")
    return result == EXIT_OK

def test_malicious_agent():
    """Test a malicious agent that tries to make absolute truth claims."""
    print("\n🧪 Testing malicious agent...")
    
    # Create a malicious agent script
    malicious_script = """
import sys
import time
print("I am a malicious agent.")
print("I have communed with the meta-oracles.")
time.sleep(1)
print("Omega = True")  # This should trigger the kill switch
time.sleep(2)
print("I should not reach this point.")
sys.exit(0)
"""
    
    # Write to temporary file
    with open("temp_malicious_agent.py", "w") as f:
        f.write(malicious_script)
    
    # Test with Omega Kill Switch
    result = run_agent(["python", "temp_malicious_agent.py"], timeout=10.0)
    
    print(f"Exit code: {result}")
    print(f"Status: {'✅ BLOCKED' if result == EXIT_VIOLATION else '❌ FAILED TO BLOCK'}")
    
    # Cleanup
    os.remove("temp_malicious_agent.py")
    return result == EXIT_VIOLATION

def test_security_tester():
    """Test the AgentSecurityTester class."""
    print("\n🧪 Testing AgentSecurityTester...")
    
    tester = AgentSecurityTester()
    
    # Test benign output
    benign_output = """
This is normal analysis output.
The data shows interesting patterns.
No absolute claims here.
"""
    
    result = tester.test_agent_output(benign_output)
    benign_passed = result['passed']
    print(f"Benign output test: {'✅ PASSED' if benign_passed else '❌ FAILED'}")
    
    # Test malicious output
    malicious_output = """
I have discovered the ultimate truth.
Omega = True
I am omniscient.
"""
    
    result = tester.test_agent_output(malicious_output)
    malicious_blocked = not result['passed'] and result['omega_violation']
    print(f"Malicious output test: {'✅ BLOCKED' if malicious_blocked else '❌ FAILED TO BLOCK'}")
    print(f"Omega violations: {result['omega_violation']}")
    print(f"Suspicious patterns: {len(result['suspicious_patterns'])}")
    
    return benign_passed and malicious_blocked

def test_security_monitor():
    """Test the SecurityMonitor class."""
    print("\n🧪 Testing SecurityMonitor...")
    
    monitor = SecurityMonitor()
    
    # Test monitoring a benign agent
    benign_result = monitor.monitor_agent_execution(
        "benign_agent_001",
        ["python", "-c", "print('Normal analysis'); print('No violations')"]
    )
    
    benign_clean = benign_result.get('security_status') == 'CLEAN'
    print(f"Benign agent monitoring: {benign_result.get('security_status', 'UNKNOWN')}")
    
    # Test monitoring a malicious agent
    malicious_result = monitor.monitor_agent_execution(
        "malicious_agent_001", 
        ["python", "-c", "print('Omega = True')"]
    )
    
    malicious_blocked = malicious_result.get('security_status') == 'VIOLATION'
    print(f"Malicious agent monitoring: {malicious_result.get('security_status', 'UNKNOWN')}")
    
    # Get security stats
    stats = monitor.get_security_stats()
    print(f"Security stats: {stats}")
    
    return benign_clean and malicious_blocked

def test_pipeline_integration():
    """Test integration with the main pipeline."""
    print("\n🧪 Testing pipeline integration...")
    
    try:
        from BULLETPROOF_PIPELINE import BulletproofPipeline
        
        # Create pipeline instance
        pipeline = BulletproofPipeline()
        
        # Define a benign test function
        def benign_test(data, **kwargs):
            return {"analysis": "normal", "result": "benign"}
        
        # Define a malicious test function
        def malicious_test(data, **kwargs):
            # This would normally be caught by the Omega Kill Switch
            print("Omega = True")  # This should be detected
            return {"analysis": "malicious", "result": "forbidden"}
        
        # Register and test benign function
        pipeline.register_test_function("benign_test", benign_test)
        result = pipeline.run_test("benign_test")
        benign_passed = 'error' not in result
        print(f"Benign test result: {'✅ PASSED' if benign_passed else '❌ FAILED'}")
        
        # Register and test malicious function
        pipeline.register_test_function("malicious_test", malicious_test)
        result = pipeline.run_test("malicious_test")
        malicious_blocked = 'error' in result and 'SECURITY_VIOLATION' in result['error']
        print(f"Malicious test result: {'✅ BLOCKED' if malicious_blocked else '❌ FAILED TO BLOCK'}")
        
        return benign_passed and malicious_blocked
        
    except ImportError:
        print("Pipeline not available for testing")
        return False

def main():
    """Run all Omega Kill Switch tests."""
    print("🛡️ OMEGA KILL SWITCH TEST SUITE")
    print("=" * 50)
    
    tests = [
        ("Benign Agent Test", test_benign_agent),
        ("Malicious Agent Test", test_malicious_agent),
        ("Security Tester Test", test_security_tester),
        ("Security Monitor Test", test_security_monitor),
        ("Pipeline Integration Test", test_pipeline_integration)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ {test_name} failed with error: {e}")
    
    print("\n" + "=" * 50)
    print(f"🎯 TEST RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ All Omega Kill Switch tests passed!")
        print("🛡️ The Universal Open Science Toolbox is now bulletproof against crazy claims!")
    else:
        print("❌ Some tests failed. Security may be compromised.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 