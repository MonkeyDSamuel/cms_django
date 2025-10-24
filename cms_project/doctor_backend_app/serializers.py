from rest_framework import serializers
from .models import Consultation, MedicinePrescription, LabPrescription
from receptionist_backend_app.models import Appointment


class ConsultationSerializer(serializers.ModelSerializer):
    """Serializer for Consultation model"""
    
    # Include appointment and patient details
    appointment_id = serializers.SerializerMethodField()
    appointment_date = serializers.SerializerMethodField()
    patient_name = serializers.SerializerMethodField()
    patient_id = serializers.SerializerMethodField()
    patient_phone = serializers.SerializerMethodField()
    patient_age = serializers.SerializerMethodField()
    patient_gender = serializers.SerializerMethodField()
    doctor_name = serializers.SerializerMethodField()
    doctor_specialization = serializers.SerializerMethodField()
    token_no = serializers.SerializerMethodField()
    appointment_status = serializers.SerializerMethodField()
    
    class Meta:
        model = Consultation
        fields = [
            'id', 'consultationId', 'AppointmentId', 'Status', 'Notes', 'Created_At', 'Updated_At',
            'appointment_id', 'appointment_date', 'patient_name', 'patient_id', 
            'patient_phone', 'patient_age', 'patient_gender', 'doctor_name',
            'doctor_specialization', 'token_no', 'appointment_status'
        ]
        read_only_fields = ['id', 'consultationId', 'Created_At', 'Updated_At']
    
    def get_appointment_id(self, obj):
        return obj.AppointmentId.AppointmentId if obj.AppointmentId else None
    
    def get_appointment_date(self, obj):
        return obj.AppointmentId.Date if obj.AppointmentId else None
    
    def get_patient_name(self, obj):
        return obj.AppointmentId.PatientId.Name if obj.AppointmentId and obj.AppointmentId.PatientId else "No Patient"
    
    def get_patient_id(self, obj):
        return obj.AppointmentId.PatientId.PatientId if obj.AppointmentId and obj.AppointmentId.PatientId else None
    
    def get_patient_phone(self, obj):
        return obj.AppointmentId.PatientId.PhoneNumber if obj.AppointmentId and obj.AppointmentId.PatientId else None
    
    def get_patient_age(self, obj):
        return obj.AppointmentId.PatientId.Age if obj.AppointmentId and obj.AppointmentId.PatientId else None
    
    def get_patient_gender(self, obj):
        return obj.AppointmentId.PatientId.get_Gender_display() if obj.AppointmentId and obj.AppointmentId.PatientId else None
    
    def get_doctor_name(self, obj):
        if obj.AppointmentId and obj.AppointmentId.DoctorId:
            return f"Dr. {obj.AppointmentId.DoctorId.StaffId.FirstName} {obj.AppointmentId.DoctorId.StaffId.LastName}"
        return "Unknown Doctor"
    
    def get_doctor_specialization(self, obj):
        return obj.AppointmentId.DoctorId.SpecializationId.SpecializationName if obj.AppointmentId and obj.AppointmentId.DoctorId else None
    
    def get_token_no(self, obj):
        return obj.AppointmentId.TokenNo if obj.AppointmentId else None
    
    def get_appointment_status(self, obj):
        return obj.AppointmentId.Status if obj.AppointmentId else None
    
    def validate_AppointmentId(self, value):
        """Validate that the appointment exists"""
        if not Appointment.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Appointment does not exist.")
        return value


class MedicinePrescriptionSerializer(serializers.ModelSerializer):
    """Serializer for MedicinePrescription model"""
    
    # Include consultation and patient details
    consultation_id = serializers.SerializerMethodField()
    consultation_status = serializers.SerializerMethodField()
    patient_name = serializers.SerializerMethodField()
    patient_id = serializers.SerializerMethodField()
    patient_phone = serializers.SerializerMethodField()
    patient_age = serializers.SerializerMethodField()
    patient_gender = serializers.SerializerMethodField()
    appointment_id = serializers.SerializerMethodField()
    appointment_date = serializers.SerializerMethodField()
    doctor_name = serializers.SerializerMethodField()
    doctor_specialization = serializers.SerializerMethodField()
    token_no = serializers.SerializerMethodField()
    
    class Meta:
        model = MedicinePrescription
        fields = [
            'id', 'medPrescriptionId', 'consultation', 'Notes', 'Created_At', 'Updated_At',
            'consultation_id', 'consultation_status', 'patient_name', 'patient_id',
            'patient_phone', 'patient_age', 'patient_gender', 'appointment_id',
            'appointment_date', 'doctor_name', 'doctor_specialization', 'token_no'
        ]
        read_only_fields = ['id', 'medPrescriptionId', 'Created_At', 'Updated_At']
    
    def get_consultation_id(self, obj):
        return obj.consultation.consultationId if obj.consultation else None
    
    def get_consultation_status(self, obj):
        return obj.consultation.Status if obj.consultation else None
    
    def get_patient_name(self, obj):
        if obj.consultation and obj.consultation.AppointmentId and obj.consultation.AppointmentId.PatientId:
            return obj.consultation.AppointmentId.PatientId.Name
        return "No Patient"
    
    def get_patient_id(self, obj):
        if obj.consultation and obj.consultation.AppointmentId and obj.consultation.AppointmentId.PatientId:
            return obj.consultation.AppointmentId.PatientId.PatientId
        return None
    
    def get_patient_phone(self, obj):
        if obj.consultation and obj.consultation.AppointmentId and obj.consultation.AppointmentId.PatientId:
            return obj.consultation.AppointmentId.PatientId.PhoneNumber
        return None
    
    def get_patient_age(self, obj):
        if obj.consultation and obj.consultation.AppointmentId and obj.consultation.AppointmentId.PatientId:
            return obj.consultation.AppointmentId.PatientId.Age
        return None
    
    def get_patient_gender(self, obj):
        if obj.consultation and obj.consultation.AppointmentId and obj.consultation.AppointmentId.PatientId:
            return obj.consultation.AppointmentId.PatientId.get_Gender_display()
        return None
    
    def get_appointment_id(self, obj):
        if obj.consultation and obj.consultation.AppointmentId:
            return obj.consultation.AppointmentId.AppointmentId
        return None
    
    def get_appointment_date(self, obj):
        if obj.consultation and obj.consultation.AppointmentId:
            return obj.consultation.AppointmentId.Date
        return None
    
    def get_doctor_name(self, obj):
        if obj.consultation and obj.consultation.AppointmentId and obj.consultation.AppointmentId.DoctorId:
            return f"Dr. {obj.consultation.AppointmentId.DoctorId.StaffId.FirstName} {obj.consultation.AppointmentId.DoctorId.StaffId.LastName}"
        return "Unknown Doctor"
    
    def get_doctor_specialization(self, obj):
        if obj.consultation and obj.consultation.AppointmentId and obj.consultation.AppointmentId.DoctorId:
            return obj.consultation.AppointmentId.DoctorId.SpecializationId.SpecializationName
        return None
    
    def get_token_no(self, obj):
        if obj.consultation and obj.consultation.AppointmentId:
            return obj.consultation.AppointmentId.TokenNo
        return None
    
    def validate_consultation(self, value):
        """Validate that the consultation exists"""
        if not Consultation.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Consultation does not exist.")
        return value


class LabPrescriptionSerializer(serializers.ModelSerializer):
    """Serializer for LabPrescription model"""
    
    # Include consultation and patient details
    consultation_id = serializers.SerializerMethodField()
    consultation_status = serializers.SerializerMethodField()
    patient_name = serializers.SerializerMethodField()
    patient_id = serializers.SerializerMethodField()
    patient_phone = serializers.SerializerMethodField()
    patient_age = serializers.SerializerMethodField()
    patient_gender = serializers.SerializerMethodField()
    appointment_id = serializers.SerializerMethodField()
    appointment_date = serializers.SerializerMethodField()
    doctor_name = serializers.SerializerMethodField()
    doctor_specialization = serializers.SerializerMethodField()
    token_no = serializers.SerializerMethodField()
    
    class Meta:
        model = LabPrescription
        fields = [
            'id', 'labPrescriptionId', 'consultation', 'test_name', 'test_type', 
            'test_instructions', 'test_fasting_required', 'Notes', 'Created_At', 'Updated_At',
            'consultation_id', 'consultation_status', 'patient_name', 'patient_id',
            'patient_phone', 'patient_age', 'patient_gender', 'appointment_id',
            'appointment_date', 'doctor_name', 'doctor_specialization', 'token_no'
        ]
        read_only_fields = ['id', 'labPrescriptionId', 'Created_At', 'Updated_At']
    
    def get_consultation_id(self, obj):
        return obj.consultation.consultationId if obj.consultation else None
    
    def get_consultation_status(self, obj):
        return obj.consultation.Status if obj.consultation else None
    
    def get_patient_name(self, obj):
        if obj.consultation and obj.consultation.AppointmentId and obj.consultation.AppointmentId.PatientId:
            return obj.consultation.AppointmentId.PatientId.Name
        return "No Patient"
    
    def get_patient_id(self, obj):
        if obj.consultation and obj.consultation.AppointmentId and obj.consultation.AppointmentId.PatientId:
            return obj.consultation.AppointmentId.PatientId.PatientId
        return None
    
    def get_patient_phone(self, obj):
        if obj.consultation and obj.consultation.AppointmentId and obj.consultation.AppointmentId.PatientId:
            return obj.consultation.AppointmentId.PatientId.PhoneNumber
        return None
    
    def get_patient_age(self, obj):
        if obj.consultation and obj.consultation.AppointmentId and obj.consultation.AppointmentId.PatientId:
            return obj.consultation.AppointmentId.PatientId.Age
        return None
    
    def get_patient_gender(self, obj):
        if obj.consultation and obj.consultation.AppointmentId and obj.consultation.AppointmentId.PatientId:
            return obj.consultation.AppointmentId.PatientId.get_Gender_display()
        return None
    
    def get_appointment_id(self, obj):
        if obj.consultation and obj.consultation.AppointmentId:
            return obj.consultation.AppointmentId.AppointmentId
        return None
    
    def get_appointment_date(self, obj):
        if obj.consultation and obj.consultation.AppointmentId:
            return obj.consultation.AppointmentId.Date
        return None
    
    def get_doctor_name(self, obj):
        if obj.consultation and obj.consultation.AppointmentId and obj.consultation.AppointmentId.DoctorId:
            return f"Dr. {obj.consultation.AppointmentId.DoctorId.StaffId.FirstName} {obj.consultation.AppointmentId.DoctorId.StaffId.LastName}"
        return "Unknown Doctor"
    
    def get_doctor_specialization(self, obj):
        if obj.consultation and obj.consultation.AppointmentId and obj.consultation.AppointmentId.DoctorId:
            return obj.consultation.AppointmentId.DoctorId.SpecializationId.SpecializationName
        return None
    
    def get_token_no(self, obj):
        if obj.consultation and obj.consultation.AppointmentId:
            return obj.consultation.AppointmentId.TokenNo
        return None
    
    def validate_consultation(self, value):
        """Validate that the consultation exists"""
        if not Consultation.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Consultation does not exist.")
        return value

