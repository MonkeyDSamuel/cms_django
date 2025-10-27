from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

class Staff(models.Model):
    # Role choices using TextChoices (Django 3.0+)
    class RoleChoices(models.TextChoices):
        ADMIN = 'ADMIN', 'Administrator'
        RECEPTIONIST = 'REC', 'Receptionist'
        DOCTOR = 'DOC', 'Doctor'
        PHARMACIST = 'PHM', 'Pharmacist'
        LAB_TECHNICIAN = 'LTECH', 'Lab Technician'

    # Role prefix mapping for ID generation
    ROLE_PREFIX_MAP = {
        'ADMIN': 'AD',
        'REC': 'REC',
        'DOC': 'DOC',
        'PHM': 'PHM',
        'LTECH': 'LTECH',
    }

    id = models.AutoField(primary_key=True)
    StaffId = models.CharField(max_length=15, unique=True, editable=False, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Role = models.CharField(max_length=10, choices=RoleChoices.choices)
    FirstName = models.CharField(max_length=100)
    LastName = models.CharField(max_length=100)
    DOB = models.DateField()
    Gender = models.CharField(choices=[("M", "Male"), ("F", "Female"), ("O", "Other")], max_length=1)
    BloodGroup = models.CharField(max_length=3)
    Address = models.TextField()
    Email = models.EmailField()
    Contact = models.CharField(max_length=15)
    IsActive = models.BooleanField(default=True)
    CreatedAt = models.DateTimeField(auto_now_add=True)
    UpdatedAt = models.DateTimeField(auto_now=True)

    def generate_staff_id(self):
        """Generate custom StaffId based on role"""
        prefix = self.ROLE_PREFIX_MAP.get(self.Role, 'STF')
        
        # Get the latest staff member with the same role
        latest_staff = Staff.objects.filter(Role=self.Role, StaffId__isnull=False).exclude(pk=self.pk).order_by('StaffId').last()
        
        if latest_staff and latest_staff.StaffId:
            # Extract the number from the last StaffId
            try:
                last_number = int(latest_staff.StaffId[len(prefix):])
                next_number = last_number + 1
            except (ValueError, IndexError):
                next_number = 1
        else:
            next_number = 1
        
        # Format with leading zeros (4 digits)
        return f"{prefix}{next_number:04d}"

    def save(self, *args, **kwargs):
        # Generate StaffId if not present
        if not self.StaffId:
            self.StaffId = self.generate_staff_id()
        
        # Validate that StaffId is unique
        if Staff.objects.filter(StaffId=self.StaffId).exclude(pk=self.pk).exists():
            raise ValidationError(f"StaffId {self.StaffId} already exists.")
        
        super().save(*args, **kwargs)

    def clean(self):
        """Custom validation"""
        super().clean()
        
        # Ensure one-to-one relationship with User
        if Staff.objects.filter(user=self.user).exclude(pk=self.pk).exists():
            raise ValidationError("This user is already associated with another staff member.")

    def __str__(self):
        return f"{self.StaffId} - {self.FirstName} {self.LastName} ({self.get_Role_display()})"

    class Meta:
        ordering = ['StaffId']
        verbose_name = 'Staff Member'
        verbose_name_plural = 'Staff Members'


class Specialization(models.Model):
    id = models.AutoField(primary_key=True)
    SpecializationName = models.CharField(max_length=20)
    Description = models.TextField()
    IsActive = models.BooleanField(default=True)
    CreatedAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.SpecializationName

class Doctor(models.Model):
    DoctorId = models.AutoField(primary_key=True)
    StaffId = models.OneToOneField(
        Staff, 
        on_delete=models.CASCADE,
        limit_choices_to={'Role': Staff.RoleChoices.DOCTOR},
        related_name='doctor_profile'
    )
    SpecializationId = models.ForeignKey(Specialization, on_delete=models.CASCADE)
    ConsultationFee = models.DecimalField(max_digits=10, decimal_places=2)
    ConsultationDays = models.JSONField(
        default=list,
        help_text="Array of integers representing days of the week (1=Sunday, 2=Monday, etc.)"
    )
    ConsultationTime = models.CharField(
        max_length=100,
        help_text="24-hour format: HH:MM-HH:MM (e.g., 09:00-17:00)"
    )
    YearsOfExperience = models.PositiveIntegerField(default=0)
    IsAvailable = models.BooleanField(default=True)
    CreatedAt = models.DateTimeField(auto_now_add=True)
    UpdatedAt = models.DateTimeField(auto_now=True)
    
    def clean(self):
        """Ensure the staff member is a doctor"""
        super().clean()
        if self.StaffId and self.StaffId.Role != Staff.RoleChoices.DOCTOR:
            raise ValidationError("Staff member must have Doctor role to create doctor profile.")
    
    def get_consultation_days_display(self):
        """Convert integer array to day names for display"""
        day_names = ['', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        if isinstance(self.ConsultationDays, list):
            return [day_names[day] for day in self.ConsultationDays if 1 <= day <= 7]
        return []
    
    def __str__(self):
        return f"Dr. {self.StaffId.FirstName} {self.StaffId.LastName} - {self.SpecializationId.SpecializationName}"