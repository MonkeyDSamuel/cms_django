from django.db import models
from django.contrib.auth.models import User


class UserRole(models.Model):
    class RoleChoices(models.TextChoices):
        ADMIN = 'ADMIN', 'Administrator'
        RECEPTIONIST = 'REC', 'Receptionist'
        DOCTOR = 'DOC', 'Doctor'
        LAB_TECHNICIAN = 'LTECH', 'Lab Technician'

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='assigned_role')
    role = models.CharField(max_length=10, choices=RoleChoices.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"
