"""
Postman Test Collection for Admin Backend API
=============================================

This document provides comprehensive testing instructions for all admin backend endpoints.

PREREQUISITES:
1. Make sure your Django server is running: python manage.py runserver
2. You need an admin user account with proper permissions
3. Use the access token from login response in Authorization header

AUTHENTICATION SETUP:
1. Login first to get access token:
   POST http://127.0.0.1:8000/auth/login/
   Body: {"username": "your_admin_username", "password": "your_password"}
   
2. Copy the "access" token from response
3. In Postman, go to Authorization tab → Bearer Token → paste the access token

TESTING CHECKLIST:
==================

1. STAFF ENDPOINTS:
   ✓ GET /api/staff/ - Get all staff members
   ✓ GET /api/staff/{id}/ - Get specific staff member
   ✓ POST /api/staff/add/ - Add new staff member
   ✓ PUT /api/staff/update/ - Update staff member
   ✓ POST /api/staff/deactive/ - Deactivate staff member

2. DOCTOR ENDPOINTS:
   ✓ GET /api/doctor/ - Get all doctors
   ✓ GET /api/doctor/{id}/ - Get specific doctor
   ✓ POST /api/doctor/create/ - Create doctor profile
   ✓ PUT /api/doctor/update/ - Update doctor details

3. SPECIALIZATION ENDPOINTS:
   ✓ GET /api/specialization/ - Get all specializations
   ✓ POST /api/specialization/add/ - Add new specialization

DETAILED TEST INSTRUCTIONS:
===========================

=== 1. STAFF MANAGEMENT ===

A. GET ALL STAFF:
   Method: GET
   URL: http://127.0.0.1:8000/api/staff/
   Headers: Authorization: Bearer {your_access_token}
   Expected: 200 OK with staff list

B. ADD NEW STAFF:
   Method: POST
   URL: http://127.0.0.1:8000/api/staff/add/
   Headers: 
     - Authorization: Bearer {your_access_token}
     - Content-Type: application/json
   Body:
   {
     "user": {
       "username": "test_staff_001",
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
   Expected: 201 Created with staff details

C. UPDATE STAFF:
   Method: PUT
   URL: http://127.0.0.1:8000/api/staff/update/
   Headers: 
     - Authorization: Bearer {your_access_token}
     - Content-Type: application/json
   Body:
   {
     "staff_id": 1,
     "FirstName": "Updated",
     "LastName": "Name",
     "Email": "updated@example.com"
   }
   Expected: 200 OK with success message

D. DEACTIVATE STAFF:
   Method: POST
   URL: http://127.0.0.1:8000/api/staff/deactive/
   Headers: 
     - Authorization: Bearer {your_access_token}
     - Content-Type: application/json
   Body:
   {
     "staff_id": 1
   }
   Expected: 200 OK with deactivation message

=== 2. DOCTOR MANAGEMENT ===

A. GET ALL DOCTORS:
   Method: GET
   URL: http://127.0.0.1:8000/api/doctor/
   Headers: Authorization: Bearer {your_access_token}
   Expected: 200 OK with doctors list

B. CREATE DOCTOR PROFILE:
   Method: POST
   URL: http://127.0.0.1:8000/api/doctor/create/
   Headers: 
     - Authorization: Bearer {your_access_token}
     - Content-Type: application/json
   Body:
   {
     "staff_id": 1,
     "specialization_id": 1,
     "consultation_fee": 150.00,
     "consultation_days": "Monday-Friday",
     "consultation_time": "9:00 AM - 5:00 PM",
     "years_of_experience": 5,
     "is_available": true
   }
   Expected: 201 Created with doctor details

C. UPDATE DOCTOR:
   Method: PUT
   URL: http://127.0.0.1:8000/api/doctor/update/
   Headers: 
     - Authorization: Bearer {your_access_token}
     - Content-Type: application/json
   Body:
   {
     "doctor_id": 1,
     "consultation_fee": 200.00,
     "years_of_experience": 7
   }
   Expected: 200 OK with success message

=== 3. SPECIALIZATION MANAGEMENT ===

A. GET ALL SPECIALIZATIONS:
   Method: GET
   URL: http://127.0.0.1:8000/api/specialization/
   Headers: Authorization: Bearer {your_access_token}
   Expected: 200 OK with specializations list

B. ADD SPECIALIZATION:
   Method: POST
   URL: http://127.0.0.1:8000/api/specialization/add/
   Headers: 
     - Authorization: Bearer {your_access_token}
     - Content-Type: application/json
   Body:
   {
     "name": "Cardiology",
     "description": "Heart and cardiovascular system specialist",
     "is_active": true
   }
   Expected: 201 Created with specialization details

ROLE VALUES REFERENCE:
======================
Staff Roles:
- "ADMIN" - Administrator
- "REC" - Receptionist
- "DOC" - Doctor
- "PHM" - Pharmacist
- "LTECH" - Lab Technician

Gender Values:
- "M" - Male
- "F" - Female
- "O" - Other

COMMON ERROR SCENARIOS:
======================

1. "You do not have permission to perform this action."
   Solution: Ensure your user has ADMIN role in Staff table or UserRole table

2. "Username already exists"
   Solution: Use a unique username

3. "Staff member not found"
   Solution: Check if staff_id exists and is correct

4. "Specialization not found"
   Solution: Create specialization first or use correct specialization_id

5. "Invalid or expired token"
   Solution: Login again to get new access token

TROUBLESHOOTING:
===============

If you still get permission errors:
1. Check your user's role in the database
2. Ensure the user has Staff record with Role='ADMIN' OR UserRole with role='ADMIN'
3. Make sure the user account is active
4. Verify the access token is valid and not expired

To check your user's role, use:
GET http://127.0.0.1:8000/auth/check-role/
Headers: Authorization: Bearer {your_access_token}

