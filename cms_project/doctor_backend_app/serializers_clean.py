from rest_framework import serializers
from .models import Consultation, MedicinePrescription, LabPrescription, LabTest

class ConsultationSerializer(serializers.ModelSerializer):
    """Serializer for Consultation model"""
    
    # Include appointment and patient details
    appointment_id = serializers.SerializerMethodField()
    patient_name = serializers.SerializerMethodField()
    patient_id = serializers.SerializerMethodField()
    patient_phone = serializers.SerializerMethodField()
    patient_age = serializers.SerializerMethodField()
    patient_gender = serializers.SerializerMethodField()
    appointment_date = serializers.SerializerMethodField()
    doctor_name = serializers.SerializerMethodField()
    doctor_specialization = serializers.SerializerMethodField()
    token_no = serializers.SerializerMethodField()
    
    class Meta:
        model = Consultation
        fields = [
            'id', 'consultationId', 'AppointmentId', 'Status', 'Notes', 'Created_At', 'Updated_At',
            'appointment_id', 'patient_name', 'patient_id', 'patient_phone', 'patient_age', 
            'patient_gender', 'appointment_date', 'doctor_name', 'doctor_specialization', 'token_no'
        ]
        read_only_fields = ['id', 'consultationId', 'Created_At', 'Updated_At']
    
    def get_appointment_id(self, obj):
        return obj.AppointmentId.appointmentId if obj.AppointmentId else None
    
    def get_patient_name(self, obj):
        if obj.AppointmentId and obj.AppointmentId.PatientId:
            return f"{obj.AppointmentId.PatientId.FirstName} {obj.AppointmentId.PatientId.LastName}"
        return None
    
    def get_patient_id(self, obj):
        return obj.AppointmentId.PatientId.patientId if obj.AppointmentId and obj.AppointmentId.PatientId else None
    
    def get_patient_phone(self, obj):
        return obj.AppointmentId.PatientId.PhoneNumber if obj.AppointmentId and obj.AppointmentId.PatientId else None
    
    def get_patient_age(self, obj):
        return obj.AppointmentId.PatientId.Age if obj.AppointmentId and obj.AppointmentId.PatientId else None
    
    def get_patient_gender(self, obj):
        return obj.AppointmentId.PatientId.Gender if obj.AppointmentId and obj.AppointmentId.PatientId else None
    
    def get_appointment_date(self, obj):
        return obj.AppointmentId.AppointmentDate if obj.AppointmentId else None
    
    def get_doctor_name(self, obj):
        if obj.AppointmentId and obj.AppointmentId.DoctorId:
            return f"Dr. {obj.AppointmentId.DoctorId.StaffId.FirstName} {obj.AppointmentId.DoctorId.StaffId.LastName}"
        return None
    
    def get_doctor_specialization(self, obj):
        if obj.AppointmentId and obj.AppointmentId.DoctorId and obj.AppointmentId.DoctorId.SpecializationId:
            return obj.AppointmentId.DoctorId.SpecializationId.SpecializationName
        return None
    
    def get_token_no(self, obj):
        if obj.AppointmentId and obj.AppointmentId.PatientId:
            return obj.AppointmentId.PatientId.TokenNo
        return None


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
            return f"{obj.consultation.AppointmentId.PatientId.FirstName} {obj.consultation.AppointmentId.PatientId.LastName}"
        return None
    
    def get_patient_id(self, obj):
        if obj.consultation and obj.consultation.AppointmentId and obj.consultation.AppointmentId.PatientId:
            return obj.consultation.AppointmentId.PatientId.patientId
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
            return obj.consultation.AppointmentId.PatientId.Gender
        return None
    
    def get_appointment_id(self, obj):
        return obj.consultation.AppointmentId.appointmentId if obj.consultation and obj.consultation.AppointmentId else None
    
    def get_appointment_date(self, obj):
        return obj.consultation.AppointmentId.AppointmentDate if obj.consultation and obj.consultation.AppointmentId else None
    
    def get_doctor_name(self, obj):
        if obj.consultation and obj.consultation.AppointmentId and obj.consultation.AppointmentId.DoctorId:
            return f"Dr. {obj.consultation.AppointmentId.DoctorId.StaffId.FirstName} {obj.consultation.AppointmentId.DoctorId.StaffId.LastName}"
        return None
    
    def get_doctor_specialization(self, obj):
        if obj.consultation and obj.consultation.AppointmentId and obj.consultation.AppointmentId.DoctorId and obj.consultation.AppointmentId.DoctorId.SpecializationId:
            return obj.consultation.AppointmentId.DoctorId.SpecializationId.SpecializationName
        return None
    
    def get_token_no(self, obj):
        if obj.consultation and obj.consultation.AppointmentId and obj.consultation.AppointmentId.PatientId:
            return obj.consultation.AppointmentId.PatientId.TokenNo
        return None


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
    test_name = serializers.SerializerMethodField()
    test_type = serializers.SerializerMethodField()
    test_instructions = serializers.SerializerMethodField()
    test_fasting_required = serializers.SerializerMethodField()
    
    class Meta:
        model = LabPrescription
        fields = [
            'id', 'labPrescriptionId', 'consultation', 'lab_test', 'Notes', 'Created_At', 'Updated_At',
            'consultation_id', 'consultation_status', 'patient_name', 'patient_id',
            'patient_phone', 'patient_age', 'patient_gender', 'appointment_id',
            'appointment_date', 'doctor_name', 'doctor_specialization', 'token_no',
            'test_name', 'test_type', 'test_instructions', 'test_fasting_required'
        ]
        read_only_fields = ['id', 'labPrescriptionId', 'Created_At', 'Updated_At']
    
    def get_consultation_id(self, obj):
        return obj.consultation.consultationId if obj.consultation else None
    
    def get_consultation_status(self, obj):
        return obj.consultation.Status if obj.consultation else None
    
    def get_patient_name(self, obj):
        if obj.consultation and obj.consultation.AppointmentId and obj.consultation.AppointmentId.PatientId:
            return f"{obj.consultation.AppointmentId.PatientId.FirstName} {obj.consultation.AppointmentId.PatientId.LastName}"
        return None
    
    def get_patient_id(self, obj):
        if obj.consultation and obj.consultation.AppointmentId and obj.consultation.AppointmentId.PatientId:
            return obj.consultation.AppointmentId.PatientId.patientId
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
            return obj.consultation.AppointmentId.PatientId.Gender
        return None
    
    def get_appointment_id(self, obj):
        return obj.consultation.AppointmentId.appointmentId if obj.consultation and obj.consultation.AppointmentId else None
    
    def get_appointment_date(self, obj):
        return obj.consultation.AppointmentId.AppointmentDate if obj.consultation and obj.consultation.AppointmentId else None
    
    def get_doctor_name(self, obj):
        if obj.consultation and obj.consultation.AppointmentId and obj.consultation.AppointmentId.DoctorId:
            return f"Dr. {obj.consultation.AppointmentId.DoctorId.StaffId.FirstName} {obj.consultation.AppointmentId.DoctorId.StaffId.LastName}"
        return None
    
    def get_doctor_specialization(self, obj):
        if obj.consultation and obj.consultation.AppointmentId and obj.consultation.AppointmentId.DoctorId and obj.consultation.AppointmentId.DoctorId.SpecializationId:
            return obj.consultation.AppointmentId.DoctorId.SpecializationId.SpecializationName
        return None
    
    def get_token_no(self, obj):
        if obj.consultation and obj.consultation.AppointmentId and obj.consultation.AppointmentId.PatientId:
            return obj.consultation.AppointmentId.PatientId.TokenNo
        return None
    
    def get_test_name(self, obj):
        return obj.lab_test.test_name if obj.lab_test else None
    
    def get_test_type(self, obj):
        return obj.lab_test.test_type if obj.lab_test else None
    
    def get_test_instructions(self, obj):
        return obj.lab_test.test_instructions if obj.lab_test else None
    
    def get_test_fasting_required(self, obj):
        return obj.lab_test.test_fasting_required if obj.lab_test else False

