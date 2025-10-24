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
    
    class Meta:
        model = Appointment
        fields = [
            'id', 'AppointmentId', 'DoctorId', 'doctor_name', 'doctor_specialization',
            'TokenNo', 'Date', 'Status', 'Created_At'
        ]
        read_only_fields = ['id', 'AppointmentId', 'Created_At']
    
    def get_doctor_name(self, obj):
        """Get doctor's full name"""
        return f"Dr. {obj.DoctorId.StaffId.FirstName} {obj.DoctorId.StaffId.LastName}"
    
    def get_doctor_specialization(self, obj):
        """Get doctor's specialization"""
        return obj.DoctorId.SpecializationId.SpecializationName

class AppointmentCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new appointments"""
    
    class Meta:
        model = Appointment
        fields = ['DoctorId', 'TokenNo', 'Date', 'Status']
    
    def validate(self, attrs):
        """Custom validation for appointment creation"""
        doctor = attrs.get('DoctorId')
        date = attrs.get('Date')
        token_no = attrs.get('TokenNo')
        
        # Check if doctor is available
        if not doctor.IsAvailable:
            raise serializers.ValidationError("Selected doctor is not available for appointments.")
        
        # Check if appointment date is not in the past
        from django.utils import timezone
        if date < timezone.now().date():
            raise serializers.ValidationError("Appointment date cannot be in the past.")
        
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
