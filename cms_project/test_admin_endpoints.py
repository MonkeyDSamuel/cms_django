#!/usr/bin/env python3
"""
Comprehensive API Test Script for Admin Backend
==============================================

This script tests all admin backend endpoints to ensure proper authorization
and functionality. Run this after starting your Django server.

Usage:
    python test_admin_endpoints.py

Prerequisites:
1. Django server running on http://127.0.0.1:8000
2. Admin user account exists
3. Required packages: requests
"""

import requests
import json
import sys
from datetime import datetime

# Configuration
BASE_URL = "http://127.0.0.1:8000"
ADMIN_CREDENTIALS = {
    "username": "admin",  # Django superuser
    "password": "admin"   # Change this to your admin password
}
STAFF_CREDENTIALS = {
    "username": "Niha",   # Staff member with DOC role
    "password": "faith"   # Password from your test
}

class APITester:
    def __init__(self):
        self.session = requests.Session()
        self.access_token = None
        self.test_results = []
        
    def log_test(self, test_name, success, message="", response_data=None):
        """Log test results"""
        status = "[PASS]" if success else "[FAIL]"
        print(f"{status} {test_name}")
        if message:
            print(f"   {message}")
        if response_data and not success:
            print(f"   Response: {response_data}")
        
        self.test_results.append({
            "test": test_name,
            "success": success,
            "message": message,
            "timestamp": datetime.now().isoformat()
        })
    
    def authenticate(self):
        """Login and get access token"""
        print("[AUTH] Authenticating...")
        try:
            response = self.session.post(
                f"{BASE_URL}/auth/login/",
                json=ADMIN_CREDENTIALS,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                self.access_token = data.get("access")
                if self.access_token:
                    self.session.headers.update({
                        "Authorization": f"Bearer {self.access_token}",
                        "Content-Type": "application/json"
                    })
                    self.log_test("Authentication", True, f"Logged in as {ADMIN_CREDENTIALS['username']}")
                    return True
                else:
                    self.log_test("Authentication", False, "No access token in response", data)
                    return False
            else:
                self.log_test("Authentication", False, f"Login failed with status {response.status_code}", response.text)
                return False
        except Exception as e:
            self.log_test("Authentication", False, f"Exception: {str(e)}")
            return False
    
    def test_staff_endpoints(self):
        """Test all staff-related endpoints"""
        print("\n[STAFF] Testing Staff Endpoints...")
        
        # Test 1: Get all staff
        try:
            response = self.session.get(f"{BASE_URL}/api/staff/")
            if response.status_code == 200:
                data = response.json()
                staff_count = data.get("count", 0)
                self.log_test("GET /api/staff/", True, f"Found {staff_count} staff members")
            else:
                self.log_test("GET /api/staff/", False, f"Status {response.status_code}", response.text)
        except Exception as e:
            self.log_test("GET /api/staff/", False, f"Exception: {str(e)}")
        
        # Test 2: Add new staff
        new_staff_data = {
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
        
        try:
            response = self.session.post(f"{BASE_URL}/api/staff/add/", json=new_staff_data)
            if response.status_code == 201:
                data = response.json()
                staff_id = data.get("data", {}).get("staff_id")
                self.log_test("POST /api/staff/add/", True, f"Created staff with ID: {staff_id}")
                
                # Test 3: Update staff
                if staff_id:
                    update_data = {
                        "staff_id": staff_id,
                        "FirstName": "Updated",
                        "LastName": "Name",
                        "Email": "updated@example.com"
                    }
                    try:
                        response = self.session.put(f"{BASE_URL}/api/staff/update/", json=update_data)
                        if response.status_code == 200:
                            self.log_test("PUT /api/staff/update/", True, "Staff updated successfully")
                        else:
                            self.log_test("PUT /api/staff/update/", False, f"Status {response.status_code}", response.text)
                    except Exception as e:
                        self.log_test("PUT /api/staff/update/", False, f"Exception: {str(e)}")
                    
                    # Test 4: Deactivate staff
                    deactivate_data = {"staff_id": staff_id}
                    try:
                        response = self.session.post(f"{BASE_URL}/api/staff/deactive/", json=deactivate_data)
                        if response.status_code == 200:
                            self.log_test("POST /api/staff/deactive/", True, "Staff deactivated successfully")
                        else:
                            self.log_test("POST /api/staff/deactive/", False, f"Status {response.status_code}", response.text)
                    except Exception as e:
                        self.log_test("POST /api/staff/deactive/", False, f"Exception: {str(e)}")
            else:
                self.log_test("POST /api/staff/add/", False, f"Status {response.status_code}", response.text)
        except Exception as e:
            self.log_test("POST /api/staff/add/", False, f"Exception: {str(e)}")
    
    def test_doctor_endpoints(self):
        """Test all doctor-related endpoints"""
        print("\n[DOCTOR] Testing Doctor Endpoints...")
        
        # Test 1: Get all doctors
        try:
            response = self.session.get(f"{BASE_URL}/api/doctor/")
            if response.status_code == 200:
                data = response.json()
                doctor_count = data.get("count", 0)
                self.log_test("GET /api/doctor/", True, f"Found {doctor_count} doctors")
            else:
                self.log_test("GET /api/doctor/", False, f"Status {response.status_code}", response.text)
        except Exception as e:
            self.log_test("GET /api/doctor/", False, f"Exception: {str(e)}")
        
        # Test 2: Create doctor profile (requires existing staff with DOC role)
        # First, let's create a doctor staff member
        doctor_staff_data = {
            "user": {
                "username": f"test_doctor_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "password": "password123",
                "email": "doctor@example.com",
                "first_name": "Test",
                "last_name": "Doctor"
            },
            "Role": "DOC",
            "FirstName": "Test",
            "LastName": "Doctor",
            "DOB": "1985-01-15",
            "Gender": "M",
            "BloodGroup": "A+",
            "Address": "456 Doctor St, City",
            "Email": "doctor@example.com",
            "Contact": "+1234567891"
        }
        
        try:
            response = self.session.post(f"{BASE_URL}/api/staff/add/", json=doctor_staff_data)
            if response.status_code == 201:
                data = response.json()
                staff_id = data.get("data", {}).get("staff_id")
                self.log_test("POST /api/staff/add/ (Doctor)", True, f"Created doctor staff with ID: {staff_id}")
                
                # Now create doctor profile
                if staff_id:
                    # First, we need a specialization
                    specialization_data = {
                        "name": "Test Cardiology",
                        "description": "Test heart specialist",
                        "is_active": True
                    }
                    
                    try:
                        spec_response = self.session.post(f"{BASE_URL}/api/specialization/add/", json=specialization_data)
                        if spec_response.status_code == 201:
                            spec_data = spec_response.json()
                            spec_id = spec_data.get("data", {}).get("specialization_id")
                            self.log_test("POST /api/specialization/add/", True, f"Created specialization with ID: {spec_id}")
                            
                            # Now create doctor profile
                            doctor_data = {
                                "staff_id": staff_id,
                                "specialization_id": spec_id,
                                "consultation_fee": 150.00,
                                "consultation_days": "Monday-Friday",
                                "consultation_time": "9:00 AM - 5:00 PM",
                                "years_of_experience": 5,
                                "is_available": True
                            }
                            
                            try:
                                response = self.session.post(f"{BASE_URL}/api/doctor/create/", json=doctor_data)
                                if response.status_code == 201:
                                    data = response.json()
                                    doctor_id = data.get("data", {}).get("doctor_id")
                                    self.log_test("POST /api/doctor/create/", True, f"Created doctor profile with ID: {doctor_id}")
                                    
                                    # Test 3: Update doctor
                                    if doctor_id:
                                        update_data = {
                                            "doctor_id": doctor_id,
                                            "consultation_fee": 200.00,
                                            "years_of_experience": 7
                                        }
                                        try:
                                            response = self.session.put(f"{BASE_URL}/api/doctor/update/", json=update_data)
                                            if response.status_code == 200:
                                                self.log_test("PUT /api/doctor/update/", True, "Doctor updated successfully")
                                            else:
                                                self.log_test("PUT /api/doctor/update/", False, f"Status {response.status_code}", response.text)
                                        except Exception as e:
                                            self.log_test("PUT /api/doctor/update/", False, f"Exception: {str(e)}")
                                else:
                                    self.log_test("POST /api/doctor/create/", False, f"Status {response.status_code}", response.text)
                            except Exception as e:
                                self.log_test("POST /api/doctor/create/", False, f"Exception: {str(e)}")
                        else:
                            self.log_test("POST /api/specialization/add/", False, f"Status {spec_response.status_code}", spec_response.text)
                    except Exception as e:
                        self.log_test("POST /api/specialization/add/", False, f"Exception: {str(e)}")
            else:
                self.log_test("POST /api/staff/add/ (Doctor)", False, f"Status {response.status_code}", response.text)
        except Exception as e:
            self.log_test("POST /api/staff/add/ (Doctor)", False, f"Exception: {str(e)}")
    
    def test_specialization_endpoints(self):
        """Test specialization endpoints"""
        print("\n[SPEC] Testing Specialization Endpoints...")
        
        # Test 1: Get all specializations
        try:
            response = self.session.get(f"{BASE_URL}/api/specialization/")
            if response.status_code == 200:
                data = response.json()
                spec_count = data.get("count", 0)
                self.log_test("GET /api/specialization/", True, f"Found {spec_count} specializations")
            else:
                self.log_test("GET /api/specialization/", False, f"Status {response.status_code}", response.text)
        except Exception as e:
            self.log_test("GET /api/specialization/", False, f"Exception: {str(e)}")
        
        # Test 2: Add specialization
        specialization_data = {
            "name": f"Test Specialization {datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "description": "Test specialization for API testing",
            "is_active": True
        }
        
        try:
            response = self.session.post(f"{BASE_URL}/api/specialization/add/", json=specialization_data)
            if response.status_code == 201:
                data = response.json()
                spec_id = data.get("data", {}).get("specialization_id")
                self.log_test("POST /api/specialization/add/", True, f"Created specialization with ID: {spec_id}")
            else:
                self.log_test("POST /api/specialization/add/", False, f"Status {response.status_code}", response.text)
        except Exception as e:
            self.log_test("POST /api/specialization/add/", False, f"Exception: {str(e)}")
    
    def run_all_tests(self):
        """Run all tests"""
        print("[START] Starting Admin Backend API Tests")
        print("=" * 50)
        
        # Authenticate first
        if not self.authenticate():
            print("[ERROR] Authentication failed. Cannot proceed with tests.")
            return False
        
        # Run all test suites
        self.test_staff_endpoints()
        self.test_doctor_endpoints()
        self.test_specialization_endpoints()
        
        # Print summary
        print("\n" + "=" * 50)
        print("[SUMMARY] TEST SUMMARY")
        print("=" * 50)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"[PASS] Passed: {passed_tests}")
        print(f"[FAIL] Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print("\n[FAILED] FAILED TESTS:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"  - {result['test']}: {result['message']}")
        
        return failed_tests == 0

def main():
    """Main function"""
    print("Admin Backend API Test Suite")
    print("=" * 30)
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/admin/", timeout=5)
        print("[SUCCESS] Django server is running")
    except requests.exceptions.RequestException:
        print("[ERROR] Django server is not running or not accessible")
        print("Please start your Django server with: python manage.py runserver")
        sys.exit(1)
    
    # Run tests
    tester = APITester()
    success = tester.run_all_tests()
    
    if success:
        print("\n[SUCCESS] All tests passed!")
        sys.exit(0)
    else:
        print("\n[ERROR] Some tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
