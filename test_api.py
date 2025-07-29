#!/usr/bin/env python3
"""
Simple test script to verify the API endpoints are working.
Run this after starting the server with: python main.py
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_health_endpoint():
    """Test the health check endpoint."""
    print("Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_providers_endpoint():
    """Test the providers endpoint."""
    print("\nTesting providers endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/providers")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_providers_with_query():
    """Test the providers endpoint with query parameter."""
    print("\nTesting providers endpoint with query parameter...")
    try:
        response = requests.get(f"{BASE_URL}/providers?query=cardiology")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_providers_with_state_code():
    """Test the providers endpoint with stateCode parameter."""
    print("\nTesting providers endpoint with stateCode parameter...")
    try:
        response = requests.get(f"{BASE_URL}/providers?stateCode=CA")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_docs_endpoint():
    """Test the docs endpoint."""
    print("\nTesting docs endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/docs")
        print(f"Status Code: {response.status_code}")
        print("Docs endpoint is accessible!")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 50)
    print("API TEST RESULTS")
    print("=" * 50)
    
    tests = [
        ("Health Endpoint", test_health_endpoint),
        ("Providers Endpoint", test_providers_endpoint),
        ("Providers with Query", test_providers_with_query),
        ("Providers with State Code", test_providers_with_state_code),
        ("Docs Endpoint", test_docs_endpoint),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        if test_func():
            print("✅ PASSED")
            passed += 1
        else:
            print("❌ FAILED")
    
    print("\n" + "=" * 50)
    print(f"SUMMARY: {passed}/{total} tests passed")
    print("=" * 50)
    
    if passed == total:
        print("🎉 All tests passed! The API is working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the server is running.")

if __name__ == "__main__":
    main() 