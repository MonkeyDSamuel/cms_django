# Admin Module Implementation - CMS Django Project

## 🎯 Overview
The Admin module has been successfully implemented for the CMS Django project, providing comprehensive staff management functionality with user account creation, doctor profile handling, and role-based permissions.

## ✅ Features Implemented

### 1. Staff Management with User Account Creation
- **Automatic User Account Creation**: When a new staff member is added, a Django User account is automatically created
- **Username & Password Return**: The system returns the username, password, and role to the frontend
- **Auto-generated Staff IDs**: Staff IDs are generated based on role (e.g., DOC0001, REC0001, PHM0001)

### 2. Doctor-Specific Form Handling
- **Dynamic Form**: When staff role is set to "doctor", an additional form appears
- **Specialization Management**: Supports both existing and new specializations
- **Doctor Details**: Captures consultation fee, days, time, experience, and availability

### 3. Staff Update Functionality
- **For Doctors**: Updates both Staff and Doctor tables with UpdatedAt timestamp
- **For Other Roles**: Updates only Staff table with UpdatedAt timestamp

## 🔗 API Endpoints

### Admin-Specific Endpoints
```
POST   /api/admin/staff/add/                    - Create new staff with user account
PUT    /api/admin/staff/{id}/update/            - Update staff member (handles doctors too)
PATCH  /api/admin/staff/{id}/update/            - Partial update staff member
POST   /api/admin/staff/{id}/deactivate/        - Deactivate staff member
POST   /api/admin/staff/{id}/create-doctor/      - Create doctor profile for staff
POST   /api/admin/specializations/add/           - Create new specialization
GET    /api/admin/dashboard/stats/               - Get admin dashboard statistics
```

### General CRUD Endpoints
```
GET    /api/staff/              - List all staff members
POST   /api/staff/              - Create new staff member (admin only)
GET    /api/staff/{id}/         - Get specific staff member
PUT    /api/staff/{id}/         - Update staff member (admin only)
DELETE /api/staff/{id}/         - Delete staff member (admin only)

GET    /api/doctors/            - List all doctors
POST   /api/doctors/            - Create new doctor (admin only)
GET    /api/doctors/{id}/       - Get specific doctor
PUT    /api/doctors/{id}/       - Update doctor (admin only)

GET    /api/specializations/    - List all specializations
POST   /api/specializations/    - Create new specialization (admin only)
```

## 📊 Database Models

### Staff Model
- **Fields**: StaffId, user (OneToOne), Role, FirstName, LastName, DOB, Gender, BloodGroup, Address, Email, Contact, IsActive, CreatedAt, UpdatedAt
- **Auto-generated StaffId**: Based on role with sequential numbering
- **Role Choices**: ADMIN, REC (Receptionist), DOC (Doctor), PHM (Pharmacist), LTECH (Lab Technician)

### Doctor Model
- **Fields**: DoctorId, StaffId (OneToOne), SpecializationId, ConsultationFee, ConsultationDays, ConsultationTime, YearsOfExperience, IsAvailable, CreatedAt, UpdatedAt
- **Validation**: Ensures staff member has Doctor role

### Specialization Model
- **Fields**: id, SpecializationName, Description, IsActive, CreatedAt
- **Features**: Active status tracking, doctor count

## 🔐 Security & Permissions
- **Admin-only Access**: Staff creation, updates, and deletions require admin permissions
- **Authentication**: Proper Django authentication integration
- **Transaction Safety**: Database operations use transactions for data integrity

## 📝 Example API Usage

### Create New Staff
```bash
POST /api/admin/staff/add/
Content-Type: application/json

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
```

**Response:**
```json
{
    "message": "Staff member created successfully",
    "staff_id": 1,
    "staff_staff_id": "DOC0001",
    "username": "john_doe",
    "password": "securepassword123",
    "role": "DOC",
    "role_display": "Doctor",
    "full_name": "John Doe",
    "email": "john@example.com"
}
```

### Create Doctor Profile
```bash
POST /api/admin/staff/{staff_id}/create-doctor/
Content-Type: application/json

{
    "specialization": {
        "name": "Cardiology",
        "description": "Heart and cardiovascular system specialist"
    },
    "consultation_fee": 150.00,
    "consultation_days": "Monday-Friday",
    "consultation_time": "9:00 AM - 5:00 PM",
    "years_of_experience": 5,
    "is_available": true
}
```

### Update Staff (with Doctor Info)
```bash
PUT /api/admin/staff/{staff_id}/update/
Content-Type: application/json

{
    "FirstName": "John",
    "LastName": "Smith",
    "Email": "john.smith@example.com",
    "doctor": {
        "consultation_fee": 200.00,
        "years_of_experience": 7,
        "specialization_id": 1
    }
}
```

## 🚀 Getting Started

### Prerequisites
- Django 5.2.6
- Python 3.13
- MySQL database
- Required packages: django-filter, djangorestframework, requests

### Installation
1. Navigate to project directory:
   ```bash
   cd "C:\Users\ajm26\OneDrive\Desktop\Faith Infotech\CAMP5\cms_django\cms_project"
   ```

2. Install required packages:
   ```bash
   pip install django-filter djangorestframework requests
   ```

3. Run migrations:
   ```bash
   python manage.py migrate
   ```

4. Start the server:
   ```bash
   python manage.py runserver
   ```

### Testing
The server will be available at `http://localhost:8000/`

- Admin endpoints: `http://localhost:8000/api/admin/`
- General API: `http://localhost:8000/api/`
- Django Admin: `http://localhost:8000/admin/`

## 📋 File Structure
```
admin_backend_app/
├── models.py          # Database models (Staff, Doctor, Specialization)
├── views.py           # API views and admin-specific endpoints
├── serializers.py     # DRF serializers for API responses
├── urls.py            # URL routing configuration
├── admin.py           # Django admin interface
└── migrations/        # Database migrations
```

## 🎉 Status: COMPLETE
The Admin module is fully implemented and ready for frontend integration. All endpoints are functional, database migrations are applied, and the server is running successfully.

## 📞 Support
For any issues or questions regarding the Admin module implementation, refer to the detailed API documentation in `admin_backend_app/urls.py` or check the Django admin interface at `/admin/`.
