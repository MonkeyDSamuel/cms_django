from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from admin_backend_app.models import Doctor

class Patient(models.Model):
    """Patient model for receptionist module"""
    
    # Gender choices
    class GenderChoices(models.TextChoices):
        MALE = 'M', 'Male'
        FEMALE = 'F', 'Female'
        OTHER = 'O', 'Other'
    
    id = models.AutoField(primary_key=True)
    PatientId = models.CharField(max_length=10, unique=True, editable=False, blank=True)
    Name = models.CharField(max_length=100)
    Age = models.PositiveIntegerField()
    Height = models.DecimalField(max_digits=5, decimal_places=2, help_text="Height in cm")
    Weight = models.DecimalField(max_digits=5, decimal_places=2, help_text="Weight in kg")
    Gender = models.CharField(max_length=1, choices=GenderChoices.choices)
    DOB = models.DateField()
    PhoneNumber = models.CharField(max_length=15)
    EmergencyNumber = models.CharField(max_length=15)
    Address = models.TextField()
    IsActive = models.BooleanField(default=True)
    Created_At = models.DateTimeField(auto_now_add=True)
    Updated_At = models.DateTimeField(auto_now=True)

    def generate_patient_id(self):
        """Generate custom PatientId like PAT0001, PAT0002, etc."""
        prefix = "PAT"
        
        # Get the latest patient
        latest_patient = Patient.objects.filter(PatientId__isnull=False).exclude(pk=self.pk).order_by('PatientId').last()
        
        if latest_patient and latest_patient.PatientId:
            # Extract the number from the last PatientId
            try:
                last_number = int(latest_patient.PatientId[3:])  # Skip "PAT" prefix
                next_number = last_number + 1
            except (ValueError, IndexError):
                next_number = 1
        else:
            next_number = 1
        
        # Format with leading zeros (4 digits)
        return f"{prefix}{next_number:04d}"

    def save(self, *args, **kwargs):
        # Generate PatientId if not present
        if not self.PatientId:
            self.PatientId = self.generate_patient_id()
        
        # Validate that PatientId is unique
        if Patient.objects.filter(PatientId=self.PatientId).exclude(pk=self.pk).exists():
            raise ValidationError(f"PatientId {self.PatientId} already exists.")
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.PatientId} - {self.Name}"

    class Meta:
        ordering = ['PatientId']
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'


class Appointment(models.Model):
    """Appointment model for receptionist module"""
    
    # Status choices
    class StatusChoices(models.TextChoices):
        SCHEDULED = 'SCHEDULED', 'Scheduled'
        CONFIRMED = 'CONFIRMED', 'Confirmed'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        COMPLETED = 'COMPLETED', 'Completed'
        CANCELLED = 'CANCELLED', 'Cancelled'
        NO_SHOW = 'NO_SHOW', 'No Show'

    id = models.AutoField(primary_key=True)
    AppointmentId = models.CharField(max_length=10, unique=True, editable=False, blank=True)
    DoctorId = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    PatientId = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments', null=True, blank=True)
    TokenNo = models.PositiveIntegerField()
    Date = models.DateField()
    Status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.SCHEDULED)
    Created_At = models.DateTimeField(auto_now_add=True)

    def generate_appointment_id(self):
        """Generate custom AppointmentId like A00001, A00002, etc."""
        prefix = "A"
        
        # Get the latest appointment
        latest_appointment = Appointment.objects.filter(AppointmentId__isnull=False).exclude(pk=self.pk).order_by('AppointmentId').last()
        
        if latest_appointment and latest_appointment.AppointmentId:
            # Extract the number from the last AppointmentId
            try:
                last_number = int(latest_appointment.AppointmentId[1:])  # Skip "A" prefix
                next_number = last_number + 1
            except (ValueError, IndexError):
                next_number = 1
        else:
            next_number = 1
        
        # Format with leading zeros (5 digits)
        return f"{prefix}{next_number:05d}"

    def save(self, *args, **kwargs):
        # Generate AppointmentId if not present
        if not self.AppointmentId:
            self.AppointmentId = self.generate_appointment_id()
        
        # Validate that AppointmentId is unique
        if Appointment.objects.filter(AppointmentId=self.AppointmentId).exclude(pk=self.pk).exists():
            raise ValidationError(f"AppointmentId {self.AppointmentId} already exists.")
        
        super().save(*args, **kwargs)

    def __str__(self):
        patient_name = self.PatientId.Name if self.PatientId else "No Patient"
        return f"{self.AppointmentId} - Dr. {self.DoctorId.StaffId.FirstName} {self.DoctorId.StaffId.LastName} - {patient_name} - {self.Date}"

    class Meta:
        ordering = ['AppointmentId']
        verbose_name = 'Appointment'
        verbose_name_plural = 'Appointments'
