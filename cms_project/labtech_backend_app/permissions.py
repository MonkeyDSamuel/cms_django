from rest_framework import permissions


class IsLabTechnician(permissions.BasePermission):
    """
    Custom permission to allow only users with role 'LabTechnician'
    """

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and hasattr(request.user, "role")
            and request.user.role == "LabTechnician"
        )
