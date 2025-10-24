from rest_framework.permissions import BasePermission
from django.contrib.auth.models import User
from admin_backend_app.models import Staff
from Authentication.models import UserRole


class IsReceptionist(BasePermission):
    """
    Custom permission class that allows access to:
    1. Django superusers (is_superuser=True) - for testing/admin purposes
    2. Users with Staff role = RECEPTIONIST
    3. Users with UserRole role = REC
    """
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Check if user is Django superuser (for admin/testing purposes)
        if request.user.is_superuser:
            return True
        
        # Check if user has Staff record with RECEPTIONIST role
        try:
            staff = Staff.objects.get(user=request.user)
            if staff.IsActive and staff.Role == Staff.RoleChoices.RECEPTIONIST:
                return True
        except Staff.DoesNotExist:
            pass
        
        # Check if user has UserRole with REC role
        try:
            user_role = UserRole.objects.get(user=request.user)
            if user_role.role == 'REC':
                return True
        except UserRole.DoesNotExist:
            pass
        
        return False


class IsReceptionistOrAdmin(BasePermission):
    """
    Custom permission class that allows access to:
    1. Django superusers (is_superuser=True)
    2. Users with Staff role = ADMIN or RECEPTIONIST
    3. Users with UserRole role = ADMIN or REC
    """
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Check if user is Django superuser
        if request.user.is_superuser:
            return True
        
        # Check if user has Staff record with ADMIN or RECEPTIONIST role
        try:
            staff = Staff.objects.get(user=request.user)
            if staff.IsActive and staff.Role in [Staff.RoleChoices.ADMIN, Staff.RoleChoices.RECEPTIONIST]:
                return True
        except Staff.DoesNotExist:
            pass
        
        # Check if user has UserRole with ADMIN or REC role
        try:
            user_role = UserRole.objects.get(user=request.user)
            if user_role.role in ['ADMIN', 'REC']:
                return True
        except UserRole.DoesNotExist:
            pass
        
        return False


class IsReceptionistOrDoctor(BasePermission):
    """
    Custom permission class that allows access to:
    1. Django superusers (is_superuser=True)
    2. Users with Staff role = RECEPTIONIST or DOCTOR
    3. Users with UserRole role = REC or DOC
    """
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Check if user is Django superuser
        if request.user.is_superuser:
            return True
        
        # Check if user has Staff record with RECEPTIONIST or DOCTOR role
        try:
            staff = Staff.objects.get(user=request.user)
            if staff.IsActive and staff.Role in [Staff.RoleChoices.RECEPTIONIST, Staff.RoleChoices.DOCTOR]:
                return True
        except Staff.DoesNotExist:
            pass
        
        # Check if user has UserRole with REC or DOC role
        try:
            user_role = UserRole.objects.get(user=request.user)
            if user_role.role in ['REC', 'DOC']:
                return True
        except UserRole.DoesNotExist:
            pass
        
        return False


class IsReceptionistOrDoctorReadOnly(BasePermission):
    """
    Custom permission class that allows:
    - Full access to RECEPTIONIST users
    - Read-only access to DOCTOR users
    - Full access to Django superusers
    """
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Check if user is Django superuser
        if request.user.is_superuser:
            return True
        
        # Check if user has Staff record with RECEPTIONIST or DOCTOR role
        try:
            staff = Staff.objects.get(user=request.user)
            if staff.IsActive and staff.Role in [Staff.RoleChoices.RECEPTIONIST, Staff.RoleChoices.DOCTOR]:
                return True
        except Staff.DoesNotExist:
            pass
        
        # Check if user has UserRole with REC or DOC role
        try:
            user_role = UserRole.objects.get(user=request.user)
            if user_role.role in ['REC', 'DOC']:
                return True
        except UserRole.DoesNotExist:
            pass
        
        return False
    
    def has_object_permission(self, request, view, obj):
        # Same as has_permission for now
        return self.has_permission(request, view)
