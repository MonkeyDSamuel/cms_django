from django.urls import path
from .views import (
    # Staff endpoints
    get_all_staff, get_staff_by_id, add_staff, update_staff, deactivate_staff,
    # Doctor endpoints  
    get_all_doctors, get_doctor_by_id, get_doctor_by_staff_id, create_doctor, update_doctor,
    # Specialization endpoints
    get_all_specializations, add_specialization
)

urlpatterns = [
    # Staff API endpoints
    path('staff/', get_all_staff, name='get_all_staff'),
    path('staff/<int:staff_id>/', get_staff_by_id, name='get_staff_by_id'),
    path('staff/add/', add_staff, name='add_staff'),
    path('staff/update/', update_staff, name='update_staff'),
    path('staff/deactive/', deactivate_staff, name='deactivate_staff'),
    
    # Doctor API endpoints
    path('doctor/', get_all_doctors, name='get_all_doctors'),
    path('doctor/<int:doctor_id>/', get_doctor_by_id, name='get_doctor_by_id'),
    path('doctor/staff/<int:staff_id>/', get_doctor_by_staff_id, name='get_doctor_by_staff_id'),
    path('doctor/create/', create_doctor, name='create_doctor'),
    path('doctor/update/', update_doctor, name='update_doctor'),
    
    # Specialization API endpoints
    path('specialization/', get_all_specializations, name='get_all_specializations'),
    path('specialization/add/', add_specialization, name='add_specialization'),
]

"""
ADMIN BACKEND API ENDPOINTS:

=== STAFF ENDPOINTS ===
GET    /api/staff/                    - Get all staff members
GET    /api/staff/{id}/               - Get specific staff member by ID
POST   /api/staff/add/                - Add new staff member with user account
PUT    /api/staff/update/             - Update staff member details
POST   /api/staff/deactive/           - Deactivate staff member (set IsActive to false)

=== DOCTOR ENDPOINTS ===
GET    /api/doctor/                   - Get all doctors
GET    /api/doctor/{id}/              - Get specific doctor by ID
POST   /api/doctor/create/            - Create new doctor profile
PUT    /api/doctor/update/            - Update doctor details

=== SPECIALIZATION ENDPOINTS ===
GET    /api/specialization/           - Get all specializations
POST   /api/specialization/add/       - Add new specialization

=== REQUEST/RESPONSE EXAMPLES ===

1. GET ALL STAFF:
GET /api/staff/
Response:
{
    "success": true,
    "data": [...],
    "count": 5
}

2. ADD NEW STAFF:
POST /api/staff/add/
{
    "user": {
        "username": "john_doe",
        "password": "securepassword123",
        "email": "john@example.com",
        "first_name": "John",
        "last_name": "Doe"
    },
    "Role": "DOC",
    "FirstName": "John",
    "LastName": "Doe",
    "DOB": "1990-01-15",
    "Gender": "M",
    "BloodGroup": "O+",
    "Address": "123 Main St, City",
    "Email": "john@example.com",
    "Contact": "+1234567890"
}

Response:
{
    "success": true,
    "message": "Staff member created successfully",
    "data": {
        "staff_id": 1,
        "staff_staff_id": "DOC0001",
        "username": "john_doe",
        "password": "securepassword123",
        "role": "DOC",
        "role_display": "Doctor",
        "full_name": "John Doe",
        "email": "john@example.com"
    }
}

3. UPDATE STAFF:
PUT /api/staff/update/
{
    "staff_id": 1,
    "FirstName": "John",
    "LastName": "Smith",
    "Email": "john.smith@example.com"
}

4. DEACTIVATE STAFF:
POST /api/staff/deactive/
{
    "staff_id": 1
}

5. CREATE DOCTOR:
POST /api/doctor/create/
{
    "staff_id": 1,
    "specialization_id": 1,
    "consultation_fee": 150.00,
    "consultation_days": "Monday-Friday",
    "consultation_time": "9:00 AM - 5:00 PM",
    "years_of_experience": 5,
    "is_available": true
}

6. UPDATE DOCTOR:
PUT /api/doctor/update/
{
    "doctor_id": 1,
    "consultation_fee": 200.00,
    "years_of_experience": 7,
    "specialization_id": 2
}

7. ADD SPECIALIZATION:
POST /api/specialization/add/
{
    "name": "Cardiology",
    "description": "Heart and cardiovascular system specialist",
    "is_active": true
}
"""