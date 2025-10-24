#!/usr/bin/env python3
"""
Simple test to verify admin restriction in staff creation
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_admin_restriction():
    """Test that admin role is rejected in staff creation"""
    print("Testing Admin Restriction in Staff Creation")
    print("=" * 50)
    
    # Login as admin
    print("\n1. Logging in as admin...")
    login_data = {"username": "admin", "password": "admin"}
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login/", json=login_data)
        if response.status_code == 200:
            token = response.json().get('access')
            print("SUCCESS: Admin login successful")
        else:
            print(f"FAILED: Admin login failed: {response.status_code}")
            return
    except Exception as e:
        print(f"ERROR: Login failed - {e}")
        return
    
    # Test admin role rejection
    print("\n2. Testing admin role rejection...")
    headers = {"Authorization": f"Bearer {token}"}
    
    admin_staff_data = {
        "user": {
            "username": "test_admin_staff",
            "password": "testpassword123",
            "email": "testadmin@example.com",
            "first_name": "Test",
            "last_name": "Admin"
        },
        "Role": "ADMIN",
        "FirstName": "Test",
        "LastName": "Admin",
        "DOB": "1990-01-15",
        "Gender": "M",
        "BloodGroup": "O+",
        "Address": "123 Test St",
        "Email": "testadmin@example.com",
        "Contact": "+1234567890"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/staff/add/", 
                               json=admin_staff_data, 
                               headers=headers)
        
        if response.status_code == 400:
            error_msg = response.json().get('error', '')
            if 'Admin users cannot be created' in error_msg:
                print("SUCCESS: ADMIN role correctly rejected")
                print(f"Error message: {error_msg}")
            else:
                print(f"FAILED: Wrong error message: {error_msg}")
        else:
            print(f"FAILED: Expected 400 error, got {response.status_code}")
    except Exception as e:
        print(f"ERROR: Request failed - {e}")
    
    print("\n" + "=" * 50)
    print("Test completed!")

if __name__ == "__main__":
    test_admin_restriction()
