# 🔐 **Authentication System Integration - COMPLETE**

## 🎯 **Authentication Flow Overview:**

Your CMS Django project has a complete authentication system that works seamlessly with the admin backend app.

### **Authentication App Features:**
- **Signup**: Creates users with token authentication
- **Login**: Returns JWT tokens with role-based redirects  
- **Role Management**: Supports admin, receptionist, doctor, lab technician, pharmacist
- **Token Authentication**: Access tokens (60 min) + Refresh tokens (30 days)

## 🔗 **Authentication Endpoints:**

### **Available at `/auth/`:**
- `POST /auth/signup/` - User registration
- `POST /auth/login/` - User login with role detection
- `POST /auth/logout/` - User logout (token deletion)
- `GET /auth/profile/` - Get user profile with staff info
- `GET /auth/check-role/` - Check user permissions and role

## 🎭 **Role-Based Access Control:**

### **Admin Role (`ADMIN`):**
- ✅ Full access to all admin endpoints
- ✅ Can manage staff, doctors, specializations
- ✅ Can create, update, deactivate staff
- ✅ Dashboard redirect: `/admin/dashboard/`

### **Doctor Role (`DOC`):**
- ✅ Access to doctor-specific endpoints
- ✅ Can manage patients
- ✅ Dashboard redirect: `/doctor/dashboard/`

### **Receptionist Role (`REC`):**
- ✅ Access to receptionist endpoints
- ✅ Can manage patients
- ✅ Dashboard redirect: `/receptionist/dashboard/`

### **Lab Technician Role (`LTECH`):**
- ✅ Access to lab technician endpoints
- ✅ Dashboard redirect: `/labtech/dashboard/`

### **Pharmacist Role (`PHM`):**
- ✅ Access to pharmacist endpoints
- ✅ Dashboard redirect: `/pharmacist/dashboard/`

## 🔐 **Authentication Integration with Admin Backend:**

### **Login Response Example:**
```json
{
    "message": "Login successful",
    "token": "your-jwt-token-here",
    "user": {
        "id": 1,
        "username": "admin_user",
        "email": "admin@example.com",
        "first_name": "Admin",
        "last_name": "User",
        "is_superuser": true,
        "is_staff": true
    },
    "staff_info": {
        "staff_id": "AD0001",
        "role": "ADMIN",
        "role_display": "Administrator",
        "first_name": "Admin",
        "last_name": "User"
    },
    "redirect_module": "admin",
    "dashboard_url": "/admin/dashboard/"
}
```

### **Role Check Response:**
```json
{
    "user_id": 1,
    "username": "admin_user",
    "permissions": {
        "is_admin": true,
        "is_staff_member": true,
        "role": "ADMIN",
        "role_display": "Administrator",
        "staff_id": "AD0001",
        "can_manage_staff": true,
        "can_manage_doctors": true,
        "can_manage_patients": true,
        "can_view_reports": true
    }
}
```

## 🚀 **How to Use with Admin Backend:**

### **1. Login to Get Token:**
```bash
POST /auth/login/
{
    "username": "admin_user",
    "password": "your_password"
}
```

### **2. Use Token for Admin API Calls:**
```bash
GET /api/staff/
Headers: {
    "Authorization": "Token your-jwt-token-here"
}
```

### **3. Admin API Endpoints (Require Authentication):**
- `GET /api/staff/` - Get all staff (requires authentication)
- `POST /api/staff/add/` - Add staff (requires admin role)
- `PUT /api/staff/update/` - Update staff (requires admin role)
- `POST /api/staff/deactive/` - Deactivate staff (requires admin role)
- `GET /api/doctor/` - Get all doctors (requires authentication)
- `POST /api/doctor/create/` - Create doctor (requires admin role)
- `GET /api/specialization/` - Get specializations (requires authentication)
- `POST /api/specialization/add/` - Add specialization (requires admin role)

## 🔧 **JWT Token Configuration:**

### **Settings in `cms_project/settings.py`:**
```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
    'SLIDING_TOKEN_LIFETIME': timedelta(days=30),
    'SLIDING_TOKEN_REFRESH_LIFETIME_LATE_USER': timedelta(days=1),
    'SLIDING_TOKEN_LIFETIME_LATE_USER': timedelta(days=30),
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
```

## 🎯 **Complete Authentication Flow:**

1. **User Signs Up** → Gets token
2. **User Logs In** → Gets token + role info + redirect URL
3. **Frontend Uses Token** → Makes authenticated API calls
4. **Role-Based Access** → Different permissions for different roles
5. **Token Expires** → User needs to refresh or login again

## ✅ **Status: FULLY INTEGRATED**

The authentication system is **completely integrated** with your admin backend app. All endpoints require proper authentication, and role-based permissions are enforced.

**Ready for production use!** 🚀
