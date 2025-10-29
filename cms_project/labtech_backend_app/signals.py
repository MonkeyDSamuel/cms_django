from django.db.models.signals import post_save
from django.dispatch import receiver
from doctor_backend_app.models import LabPrescription
from .models import Prescription

@receiver(post_save, sender=LabPrescription)
def create_lab_prescription(sender, instance, created, **kwargs):
    """
    Automatically create a Prescription in lab module when doctor creates LabPrescription
    """
    if created:
        try:
            # Get patient and doctor info from consultation
            consultation = instance.consultation
            appointment = consultation.AppointmentId
            patient = appointment.PatientId
            doctor = appointment.DoctorId
            
            Prescription.objects.create(
                lab_prescription=instance,
                patient_name=f"{patient.FirstName} {patient.LastName}",
                patient_id=patient.PatientId,
                doctor_name=f"{doctor.FirstName} {doctor.LastName}",
                status='Pending'
            )
            print(f"✅ Auto-created lab prescription for {patient.FirstName}")
        except Exception as e:
            print(f"❌ Error creating lab prescription: {e}")