from rest_framework.permissions import BasePermission
from django.contrib.auth.models import User
from .models import Staff
from Authentication.models import UserRole


class IsAdminOrStaffAdmin(BasePermission):
    """
    Custom permission class that allows access to:
    1. Django superusers (is_superuser=True)
    2. Users with Staff role = ADMIN
    3. Users with UserRole role = ADMIN
    """
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Check if user is Django superuser
        if request.user.is_superuser:
            return True
        
        # Check if user has Staff record with ADMIN role
        try:
            staff = Staff.objects.get(user=request.user)
            if staff.IsActive and staff.Role == Staff.RoleChoices.ADMIN:
                return True
        except Staff.DoesNotExist:
            pass
        
        # Check if user has UserRole with ADMIN role
        try:
            user_role = UserRole.objects.get(user=request.user)
            if user_role.role == 'ADMIN':
                return True
        except UserRole.DoesNotExist:
            pass
        
        return False


class IsStaffMember(BasePermission):
    """
    Custom permission class that allows access to any active staff member
    """
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Check if user is Django superuser
        if request.user.is_superuser:
            return True
        
        # Check if user has Staff record
        try:
            staff = Staff.objects.get(user=request.user)
            if staff.IsActive:
                return True
        except Staff.DoesNotExist:
            pass
        
        # Check if user has UserRole
        try:
            UserRole.objects.get(user=request.user)
            return True
        except UserRole.DoesNotExist:
            pass
        
        return False

