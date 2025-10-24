# Receptionist Module - Role-Based Access Control

## 🎯 **Overview**

The Receptionist Module has been successfully implemented with **role-based access control** that ensures only users with **Receptionist** role can access the receptionist module routes and functions.

## 🔐 **Authentication & Authorization**

### **Role-Based Access Control**

The receptionist module uses custom permission classes to control access:

#### **Permission Classes:**

1. **`IsReceptionist`** - Allows access to:
   - Django superusers (for admin/testing purposes)
   - Users with Staff role = `RECEPTIONIST`
   - Users with UserRole role = `REC`

2. **`IsReceptionistOrAdmin`** - Allows access to:
   - Django superusers
   - Users with Staff role = `ADMIN` or `RECEPTIONIST`
   - Users with UserRole role = `ADMIN` or `REC`

### **Authentication Flow:**

1. **Login Process:**
   - User logs in via `/auth/login/`
   - System checks both `Staff` table and `UserRole` table
   - Returns role information and JWT tokens

2. **Access Control:**
   - All receptionist endpoints require authentication
   - Permission classes verify user role before allowing access
   - Returns `403 Forbidden` for unauthorized users

## 📋 **Models**

### **Patient Model**
```python
- id (Primary Key)
- PatientId (Auto-generated: PAT0001, PAT0002, ...)
- Name, Age, Height, Weight, Gender, DOB
- PhoneNumber, EmergencyNumber, Address
- IsActive, Created_At, Updated_At
```

### **Appointment Model**
```python
- id (Primary Key)
- AppointmentId (Auto-generated: A00001, A00002, ...)
- DoctorId (Foreign Key to Doctor)
- TokenNo, Date, Status
- Created_At
```

## 🔗 **API Endpoints**

### **Base URL:** `/api/receptionist/`

#### **Patient Endpoints:**
- `GET /patients/` - List all patients (Receptionist only)
- `POST /patients/` - Create new patient (Receptionist only)
- `GET /patients/{id}/` - Get specific patient (Receptionist only)

#### **Appointment Endpoints:**
- `GET /appointments/` - List all appointments (Receptionist only)
- `POST /appointments/` - Create new appointment (Receptionist only)
- `GET /appointments/{id}/` - Get specific appointment (Receptionist only)

#### **Doctor Endpoints:**
- `GET /doctors/` - List available doctors for booking (Receptionist only)

## 🧪 **Testing Results**

### **Access Control Verification:**

| User Type | Username | Role | Patients | Appointments | Doctors | Result |
|-----------|----------|------|----------|--------------|---------|---------|
| Admin | admin | ADMIN | ✅ 200 | ✅ 200 | ✅ 200 | **Allowed** |
| Doctor | Niha | DOC | ❌ 403 | ❌ 403 | ❌ 403 | **Forbidden** |
| Receptionist | receptionist1 | REC | ✅ 200 | ✅ 200 | ✅ 200 | **Allowed** |

### **Test Credentials:**

#### **Receptionist User:**
- **Username:** `receptionist1`
- **Password:** `receptionist123`
- **Role:** `REC` (Receptionist)
- **Access:** Full access to all receptionist endpoints

#### **Admin User:**
- **Username:** `admin`
- **Password:** `admin`
- **Role:** `ADMIN`
- **Access:** Full access to all endpoints (including receptionist)

#### **Doctor User:**
- **Username:** `Niha`
- **Password:** `faith`
- **Role:** `DOC`
- **Access:** Forbidden from receptionist endpoints

## 🚀 **Features Implemented**

### ✅ **Role-Based Access Control**
- Custom permission classes for receptionist-only access
- Integration with existing authentication system
- Support for both Staff and UserRole tables

### ✅ **Auto-Generated IDs**
- PatientId: PAT0001, PAT0002, PAT0003...
- AppointmentId: A00001, A00002, A00003...

### ✅ **Data Validation**
- Appointment validation (no past dates, unique token numbers)
- Patient data validation
- Foreign key relationships

### ✅ **Filtering & Search**
- Patients: Filter by gender, status; search by name, phone
- Appointments: Filter by status, doctor, date; search by appointment ID

### ✅ **Admin Interface**
- Django admin integration for both models
- Proper display and filtering options

## 📁 **Files Created/Modified**

### **New Files:**
- `receptionist_backend_app/permissions.py` - Custom permission classes
- `receptionist_backend_app/models.py` - Patient and Appointment models
- `receptionist_backend_app/serializers.py` - API serializers
- `receptionist_backend_app/views.py` - API views with role-based permissions
- `receptionist_backend_app/urls.py` - URL routing
- `receptionist_backend_app/admin.py` - Admin interface

### **Modified Files:**
- `cms_project/urls.py` - Added receptionist URL routing
- Database migrations created and applied

## 🔧 **Usage Examples**

### **Login as Receptionist:**
```bash
POST /auth/login/
{
    "username": "receptionist1",
    "password": "receptionist123"
}
```

### **Create Patient (Receptionist only):**
```bash
POST /api/receptionist/patients/
Authorization: Bearer <token>
{
    "Name": "John Doe",
    "Age": 30,
    "Height": 175.5,
    "Weight": 70.0,
    "Gender": "M",
    "DOB": "1994-01-15",
    "PhoneNumber": "+1234567890",
    "EmergencyNumber": "+0987654321",
    "Address": "123 Main St, City, State",
    "IsActive": true
}
```

### **Create Appointment (Receptionist only):**
```bash
POST /api/receptionist/appointments/
Authorization: Bearer <token>
{
    "DoctorId": 1,
    "TokenNo": 1,
    "Date": "2024-12-25",
    "Status": "SCHEDULED"
}
```

## 🎉 **Status: COMPLETE**

The Receptionist Module is **fully functional** with proper role-based access control. Only users with Receptionist role can access the receptionist module routes and functions, ensuring proper security and data access control.

### **Next Steps:**
1. **Frontend Integration** - Connect React frontend to receptionist endpoints
2. **Additional Features** - Add update/delete endpoints if needed
3. **Reporting** - Add appointment and patient reports
4. **Notifications** - Add appointment reminders and notifications

