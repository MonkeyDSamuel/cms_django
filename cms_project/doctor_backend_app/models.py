from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from receptionist_backend_app.models import Appointment


class Consultation(models.Model):
    """Consultation model for doctor module"""
    
    # Status choices for consultation
    class StatusChoices(models.TextChoices):
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        COMPLETED = 'COMPLETED', 'Completed'
        CANCELLED = 'CANCELLED', 'Cancelled'
        ON_HOLD = 'ON_HOLD', 'On Hold'
    
    id = models.AutoField(primary_key=True)
    consultationId = models.CharField(max_length=10, unique=True, editable=False, blank=True)
    AppointmentId = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='consultations')
    Status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.IN_PROGRESS)
    Notes = models.TextField(blank=True, null=True, help_text="Doctor's notes for this consultation")
    Created_At = models.DateTimeField(auto_now_add=True)
    Updated_At = models.DateTimeField(auto_now=True)

    def generate_consultation_id(self):
        """Generate custom consultationId like C00001, C00002, etc."""
        prefix = "C"
        
        # Get the latest consultation
        latest_consultation = Consultation.objects.filter(consultationId__isnull=False).exclude(pk=self.pk).order_by('consultationId').last()
        
        if latest_consultation and latest_consultation.consultationId:
            # Extract the number from the last consultationId
            try:
                last_number = int(latest_consultation.consultationId[1:])  # Skip "C" prefix
                next_number = last_number + 1
            except (ValueError, IndexError):
                next_number = 1
        else:
            next_number = 1
        
        # Format with leading zeros (5 digits)
        return f"{prefix}{next_number:05d}"

    def save(self, *args, **kwargs):
        # Generate consultationId if not present
        if not self.consultationId:
            self.consultationId = self.generate_consultation_id()
        
        # Validate that consultationId is unique
        if Consultation.objects.filter(consultationId=self.consultationId).exclude(pk=self.pk).exists():
            raise ValidationError(f"consultationId {self.consultationId} already exists.")
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.consultationId} - {self.AppointmentId}"

    class Meta:
        ordering = ['consultationId']
        verbose_name = 'Consultation'
        verbose_name_plural = 'Consultations'


class MedicinePrescription(models.Model):
    """Medicine Prescription model for doctor module"""
    
    id = models.AutoField(primary_key=True)
    medPrescriptionId = models.CharField(max_length=15, unique=True, editable=False, blank=True)
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE, related_name='medicine_prescriptions')
    Notes = models.TextField(blank=True, null=True, help_text="Doctor's notes for this medicine prescription")
    Created_At = models.DateTimeField(auto_now_add=True)
    Updated_At = models.DateTimeField(auto_now=True)

    def generate_med_prescription_id(self):
        """Generate custom medPrescriptionId like MEDP00001, MEDP00002, etc."""
        prefix = "MEDP"
        
        # Get the latest medicine prescription
        latest_prescription = MedicinePrescription.objects.filter(medPrescriptionId__isnull=False).exclude(pk=self.pk).order_by('medPrescriptionId').last()
        
        if latest_prescription and latest_prescription.medPrescriptionId:
            # Extract the number from the last medPrescriptionId
            try:
                last_number = int(latest_prescription.medPrescriptionId[4:])  # Skip "MEDP" prefix
                next_number = last_number + 1
            except (ValueError, IndexError):
                next_number = 1
        else:
            next_number = 1
        
        # Format with leading zeros (5 digits)
        return f"{prefix}{next_number:05d}"

    def save(self, *args, **kwargs):
        # Generate medPrescriptionId if not present
        if not self.medPrescriptionId:
            self.medPrescriptionId = self.generate_med_prescription_id()
        
        # Validate that medPrescriptionId is unique
        if MedicinePrescription.objects.filter(medPrescriptionId=self.medPrescriptionId).exclude(pk=self.pk).exists():
            raise ValidationError(f"medPrescriptionId {self.medPrescriptionId} already exists.")
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.medPrescriptionId} - {self.consultation.consultationId}"

    class Meta:
        ordering = ['medPrescriptionId']
        verbose_name = 'Medicine Prescription'
        verbose_name_plural = 'Medicine Prescriptions'


class LabPrescription(models.Model):
    """Lab Prescription model for doctor module"""
    
    id = models.AutoField(primary_key=True)
    labPrescriptionId = models.CharField(max_length=15, unique=True, editable=False, blank=True)
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE, related_name='lab_prescriptions')
    test_name = models.CharField(max_length=200, default="", help_text="Name of the lab test")
    test_type = models.CharField(max_length=100, default="", help_text="Type of lab test (Blood, Urine, etc.)")
    test_instructions = models.TextField(default="", help_text="Instructions for the test")
    test_fasting_required = models.BooleanField(default=False, help_text="Whether fasting is required before the test")
    Notes = models.TextField(blank=True, null=True, help_text="Doctor's notes for this lab test prescription")
    Created_At = models.DateTimeField(auto_now_add=True)
    Updated_At = models.DateTimeField(auto_now=True)

    def generate_lab_prescription_id(self):
        """Generate custom labPrescriptionId like LABP00001, LABP00002, etc."""
        prefix = "LABP"
        
        # Get the latest lab prescription
        latest_prescription = LabPrescription.objects.filter(labPrescriptionId__isnull=False).exclude(pk=self.pk).order_by('labPrescriptionId').last()
        
        if latest_prescription and latest_prescription.labPrescriptionId:
            # Extract the number from the last labPrescriptionId
            try:
                last_number = int(latest_prescription.labPrescriptionId[4:])  # Skip "LABP" prefix
                next_number = last_number + 1
            except (ValueError, IndexError):
                next_number = 1
        else:
            next_number = 1
        
        # Format with leading zeros (5 digits)
        return f"{prefix}{next_number:05d}"

    def save(self, *args, **kwargs):
        # Generate labPrescriptionId if not present
        if not self.labPrescriptionId:
            self.labPrescriptionId = self.generate_lab_prescription_id()
        
        # Validate that labPrescriptionId is unique
        if LabPrescription.objects.filter(labPrescriptionId=self.labPrescriptionId).exclude(pk=self.pk).exists():
            raise ValidationError(f"labPrescriptionId {self.labPrescriptionId} already exists.")
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.labPrescriptionId} - {self.consultation.consultationId}"

    class Meta:
        ordering = ['labPrescriptionId']
        verbose_name = 'Lab Prescription'
        verbose_name_plural = 'Lab Prescriptions'
