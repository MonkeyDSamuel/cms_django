#!/usr/bin/env python3
"""
Simple API Test Script for Admin Backend
========================================

This script tests the admin backend endpoints with different user types.
"""

import requests
import json
import sys
from datetime import datetime

# Configuration
BASE_URL = "http://127.0.0.1:8000"

def test_endpoint(method, url, headers=None, data=None, expected_status=200):
    """Test a single endpoint"""
    try:
        if method.upper() == "GET":
            response = requests.get(url, headers=headers)
        elif method.upper() == "POST":
            response = requests.post(url, headers=headers, json=data)
        elif method.upper() == "PUT":
            response = requests.put(url, headers=headers, json=data)
        else:
            return False, f"Unsupported method: {method}"
        
        success = response.status_code == expected_status
        message = f"Status: {response.status_code}"
        if not success:
            message += f", Response: {response.text[:200]}"
        
        return success, message
    except Exception as e:
        return False, f"Exception: {str(e)}"

def login_user(username, password):
    """Login and get access token"""
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login/",
            json={"username": username, "password": password},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            access_token = data.get("access")
            if access_token:
                return True, access_token, data.get("role", "Unknown")
            else:
                return False, None, "No access token"
        else:
            return False, None, f"Login failed: {response.text}"
    except Exception as e:
        return False, None, f"Exception: {str(e)}"

def test_user_permissions(username, password, user_type):
    """Test all endpoints for a specific user"""
    print(f"\n[TESTING] {user_type} - {username}")
    print("-" * 50)
    
    # Login
    success, token, role = login_user(username, password)
    if not success:
        print(f"[FAIL] Login failed: {role}")
        return False
    
    print(f"[PASS] Login successful - Role: {role}")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Test results
    results = []
    
    # Test 1: Get all staff
    success, message = test_endpoint("GET", f"{BASE_URL}/api/staff/", headers)
    results.append(("GET /api/staff/", success, message))
    
    # Test 2: Get all doctors
    success, message = test_endpoint("GET", f"{BASE_URL}/api/doctor/", headers)
    results.append(("GET /api/doctor/", success, message))
    
    # Test 3: Get all specializations
    success, message = test_endpoint("GET", f"{BASE_URL}/api/specialization/", headers)
    results.append(("GET /api/specialization/", success, message))
    
    # Test 4: Add staff (admin only)
    staff_data = {
        "user": {
            "username": f"test_staff_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "password": "password123",
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "Staff"
        },
        "Role": "REC",
        "FirstName": "Test",
        "LastName": "Staff",
        "DOB": "1990-01-15",
        "Gender": "M",
        "BloodGroup": "O+",
        "Address": "123 Test St, City",
        "Email": "test@example.com",
        "Contact": "+1234567890"
    }
    success, message = test_endpoint("POST", f"{BASE_URL}/api/staff/add/", headers, staff_data, 201)
    results.append(("POST /api/staff/add/", success, message))
    
    # Test 5: Add specialization (admin only)
    spec_data = {
        "name": f"Test{datetime.now().strftime('%H%M%S')}",
        "description": "Test specialization",
        "is_active": True
    }
    success, message = test_endpoint("POST", f"{BASE_URL}/api/specialization/add/", headers, spec_data, 201)
    results.append(("POST /api/specialization/add/", success, message))
    
    # Print results
    for test_name, success, message in results:
        status = "[PASS]" if success else "[FAIL]"
        print(f"{status} {test_name}")
        if not success:
            print(f"   {message}")
    
    return all(success for _, success, _ in results)

def main():
    """Main function"""
    print("Admin Backend API Permission Test")
    print("=" * 40)
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/admin/", timeout=5)
        print("[SUCCESS] Django server is running")
    except requests.exceptions.RequestException:
        print("[ERROR] Django server is not running")
        print("Please start your Django server with: python manage.py runserver")
        sys.exit(1)
    
    # Test different user types
    test_cases = [
        ("admin", "admin", "Django Superuser"),
        ("Niha", "faith", "Staff Member (DOC role)")
    ]
    
    all_passed = True
    for username, password, user_type in test_cases:
        passed = test_user_permissions(username, password, user_type)
        all_passed = all_passed and passed
    
    print("\n" + "=" * 40)
    if all_passed:
        print("[SUCCESS] All tests passed!")
    else:
        print("[ERROR] Some tests failed!")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
