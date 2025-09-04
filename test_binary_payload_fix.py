#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test case for issue #1: Request with binary payload fails due to calling to_native_string"""

import sys
import os

# Add the requests module to path  
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import warnings
warnings.filterwarnings('ignore')  # Suppress syntax warnings from legacy code

import requests

def test_binary_payload():
    """Test that binary data (bytes) can be used as request data without errors.
    
    This test reproduces the issue reported where:
    requests.put("http://httpbin.org/put", data=u"ööö".encode("utf-8"))
    
    Works with requests 2.8.1 but fails with 2.9.0 due to to_native_string
    trying to decode binary data with ASCII encoding.
    """
    print("Testing binary payload fix...")
    
    # Create UTF-8 encoded binary data 
    binary_data = u"ööö".encode("utf-8")
    print(f"Binary data: {repr(binary_data)}")
    print(f"Type: {type(binary_data)}")
    
    try:
        # Create request with binary data (without actually sending it)
        req = requests.Request('PUT', 'http://httpbin.org/put', data=binary_data)
        prepared = req.prepare()
        
        # Verify the request was prepared successfully
        assert prepared.body == binary_data, f"Expected {repr(binary_data)}, got {repr(prepared.body)}"
        assert isinstance(prepared.body, bytes), f"Expected bytes, got {type(prepared.body)}"
        
        print(f"✓ SUCCESS: Binary data preserved as {type(prepared.body)}: {repr(prepared.body)}")
        return True
        
    except Exception as e:
        print(f"✗ FAILED: {e}")
        return False

def test_string_payload():
    """Test that string data still works correctly after the fix."""
    print("\nTesting string payload (regression test)...")
    
    # Create string data
    string_data = "hello world"
    print(f"String data: {repr(string_data)}")
    print(f"Type: {type(string_data)}")
    
    try:
        # Create request with string data
        req = requests.Request('PUT', 'http://httpbin.org/put', data=string_data)
        prepared = req.prepare()
        
        # Verify the request was prepared successfully
        assert prepared.body == string_data, f"Expected {repr(string_data)}, got {repr(prepared.body)}"
        assert isinstance(prepared.body, str), f"Expected str, got {type(prepared.body)}"
        
        print(f"✓ SUCCESS: String data preserved as {type(prepared.body)}: {repr(prepared.body)}")
        return True
        
    except Exception as e:
        print(f"✗ FAILED: {e}")
        return False

def test_unicode_string_payload():
    """Test that Unicode strings work correctly."""
    print("\nTesting Unicode string payload...")
    
    # Create Unicode string data
    unicode_data = u"ööö"  # Unicode string, not bytes
    print(f"Unicode data: {repr(unicode_data)}")
    print(f"Type: {type(unicode_data)}")
    
    try:
        # Create request with Unicode string data
        req = requests.Request('PUT', 'http://httpbin.org/put', data=unicode_data)
        prepared = req.prepare()
        
        # Verify the request was prepared successfully  
        assert prepared.body == unicode_data, f"Expected {repr(unicode_data)}, got {repr(prepared.body)}"
        assert isinstance(prepared.body, str), f"Expected str, got {type(prepared.body)}"
        
        print(f"✓ SUCCESS: Unicode string preserved as {type(prepared.body)}: {repr(prepared.body)}")
        return True
        
    except Exception as e:
        print(f"✗ FAILED: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Testing fix for binary payload issue")
    print("=" * 60)
    
    all_tests_passed = True
    
    all_tests_passed &= test_binary_payload()
    all_tests_passed &= test_string_payload() 
    all_tests_passed &= test_unicode_string_payload()
    
    print("\n" + "=" * 60)
    if all_tests_passed:
        print("🎉 ALL TESTS PASSED! The fix is working correctly.")
        sys.exit(0)
    else:
        print("❌ SOME TESTS FAILED!")
        sys.exit(1)