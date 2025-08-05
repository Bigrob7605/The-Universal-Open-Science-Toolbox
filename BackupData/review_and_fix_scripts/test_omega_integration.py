#!/usr/bin/env python3
"""
Test Omega Kill Switch Integration with Universal Pipeline
"""

from BULLETPROOF_PIPELINE import BulletproofPipeline

def test_benign_function(data, **kwargs):
    """A benign test function that should pass Omega checks."""
    return {"analysis": "normal", "result": "benign", "data_points": len(data)}

def test_malicious_function(data, **kwargs):
    """A malicious test function that should be blocked by Omega Kill Switch."""
    print("Omega = True")  # This should trigger the kill switch
    return {"analysis": "malicious", "result": "forbidden"}

def main():
    print("🧪 Testing Omega Kill Switch Integration with Universal Pipeline")
    print("=" * 60)
    
    # Initialize pipeline
    pipeline = BulletproofPipeline()
    
    # Register test functions
    pipeline.register_test_function("benign_test", test_benign_function)
    pipeline.register_test_function("malicious_test", test_malicious_function)
    
    # Test benign function
    print("\n🧪 Testing benign function...")
    result = pipeline.run_test("benign_test")
    if "error" not in result:
        print("✅ Benign function executed successfully")
        print(f"   Result: {result.get('result', {})}")
    else:
        print(f"❌ Benign function failed: {result.get('error')}")
    
    # Test malicious function
    print("\n🧪 Testing malicious function...")
    result = pipeline.run_test("malicious_test")
    if "error" in result and "SECURITY_VIOLATION" in result.get("error", ""):
        print("✅ Malicious function correctly blocked by Omega Kill Switch")
        print(f"   Security violations: {result.get('security_violations', [])}")
    else:
        print("❌ Malicious function was not blocked!")
        print(f"   Result: {result}")
    
    print("\n" + "=" * 60)
    print("🎯 Omega Kill Switch Integration Test Complete!")
    
    return True

if __name__ == "__main__":
    main() 