from rest_framework import serializers
from .models import Patient, Appointment
from admin_backend_app.models import Doctor

class PatientSerializer(serializers.ModelSerializer):
    """Serializer for Patient model"""
    
    class Meta:
        model = Patient
        fields = [
            'id', 'PatientId', 'Name', 'Age', 'Height', 'Weight', 
            'Gender', 'DOB', 'PhoneNumber', 'EmergencyNumber', 
            'Address', 'IsActive', 'Created_At', 'Updated_At'
        ]
        read_only_fields = ['id', 'PatientId', 'Created_At', 'Updated_At']

class PatientCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new patients"""
    
    class Meta:
        model = Patient
        fields = [
            'Name', 'Age', 'Height', 'Weight', 'Gender', 'DOB',
            'PhoneNumber', 'EmergencyNumber', 'Address', 'IsActive'
        ]

class AppointmentSerializer(serializers.ModelSerializer):
    """Serializer for Appointment model"""
    
    # Include doctor details in the response
    doctor_name = serializers.SerializerMethodField()
    doctor_specialization = serializers.SerializerMethodField()
    
    # Include patient details in the response
    patient_name = serializers.SerializerMethodField()
    patient_id = serializers.SerializerMethodField()
    patient_phone = serializers.SerializerMethodField()
    patient_age = serializers.SerializerMethodField()
    patient_gender = serializers.SerializerMethodField()
    
    class Meta:
        model = Appointment
        fields = [
            'id', 'AppointmentId', 'DoctorId', 'PatientId', 'doctor_name', 'doctor_specialization',
            'patient_name', 'patient_id', 'patient_phone', 'patient_age', 'patient_gender',
            'TokenNo', 'Date', 'Status', 'Created_At'
        ]
        read_only_fields = ['id', 'AppointmentId', 'Created_At']
    
    def get_doctor_name(self, obj):
        """Get doctor's full name"""
        return f"Dr. {obj.DoctorId.StaffId.FirstName} {obj.DoctorId.StaffId.LastName}"
    
    def get_doctor_specialization(self, obj):
        """Get doctor's specialization"""
        return obj.DoctorId.SpecializationId.SpecializationName
    
    def get_patient_name(self, obj):
        """Get patient's full name"""
        return obj.PatientId.Name if obj.PatientId else "No Patient"
    
    def get_patient_id(self, obj):
        """Get patient's ID"""
        return obj.PatientId.PatientId if obj.PatientId else "N/A"
    
    def get_patient_phone(self, obj):
        """Get patient's phone number"""
        return obj.PatientId.PhoneNumber if obj.PatientId else "N/A"
    
    def get_patient_age(self, obj):
        """Get patient's age"""
        return obj.PatientId.Age if obj.PatientId else "N/A"
    
    def get_patient_gender(self, obj):
        """Get patient's gender"""
        return obj.PatientId.get_Gender_display() if obj.PatientId else "N/A"

class AppointmentCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new appointments"""
    
    class Meta:
        model = Appointment
        fields = ['DoctorId', 'PatientId', 'TokenNo', 'Date', 'Status']
    
    def validate(self, attrs):
        """Custom validation for appointment creation"""
        doctor = attrs.get('DoctorId')
        date = attrs.get('Date')
        token_no = attrs.get('TokenNo')
        
        # Check if doctor is available
        if not doctor.IsAvailable:
            raise serializers.ValidationError("Selected doctor is not available for appointments.")
        
        # Check if doctor's staff is active
        if not doctor.StaffId.IsActive:
            raise serializers.ValidationError("Selected doctor's account is inactive.")
        
        # Check if appointment date is not in the past
        from django.utils import timezone
        if date < timezone.now().date():
            raise serializers.ValidationError("Appointment date cannot be in the past.")
        
        # Check doctor's consultation days and time
        from datetime import datetime
        appointment_date = date
        day_name = appointment_date.strftime('%A')  # Get day name (Monday, Tuesday, etc.)
        
        # Check if the appointment day matches doctor's consultation days
        consultation_days = doctor.ConsultationDays.lower()
        if day_name.lower() not in consultation_days:
            raise serializers.ValidationError(
                f"Doctor is not available on {day_name}. Available days: {doctor.ConsultationDays}"
            )
        
        # Check if token number is already taken for the same doctor and date
        existing_appointment = Appointment.objects.filter(
            DoctorId=doctor,
            Date=date,
            TokenNo=token_no
        ).exists()
        
        if existing_appointment:
            raise serializers.ValidationError(
                f"Token number {token_no} is already taken for this doctor on {date}."
            )
        
        return attrs
