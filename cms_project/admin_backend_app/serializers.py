from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Staff, Specialization, Doctor


class UserSerializer(serializers.ModelSerializer):
    """Serializer for Django User model"""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'date_joined']
        read_only_fields = ['id', 'date_joined']


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new users with password"""
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password_confirm']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class StaffSerializer(serializers.ModelSerializer):
    """Serializer for Staff model with nested user information"""
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    role_display = serializers.CharField(source='get_Role_display', read_only=True)
    age = serializers.SerializerMethodField()
    
    class Meta:
        model = Staff
        fields = [
            'id', 'StaffId', 'user', 'user_id', 'Role', 'role_display',
            'FirstName', 'LastName', 'DOB', 'age', 'Gender', 'BloodGroup',
            'Address', 'Email', 'Contact', 'IsActive', 'CreatedAt', 'UpdatedAt'
        ]
        read_only_fields = ['id', 'StaffId', 'CreatedAt', 'UpdatedAt']
    
    def get_age(self, obj):
        """Calculate age from date of birth"""
        from datetime import date
        if obj.DOB:
            today = date.today()
            return today.year - obj.DOB.year - ((today.month, today.day) < (obj.DOB.month, obj.DOB.day))
        return None
    
    def validate_user_id(self, value):
        """Validate that user exists and is not already associated with another staff"""
        try:
            user = User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User does not exist")
        
        # Check if user is already associated with another staff member
        if Staff.objects.filter(user=user).exists():
            raise serializers.ValidationError("This user is already associated with another staff member")
        
        return value


class StaffCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating staff with user account"""
    user = UserCreateSerializer()
    
    class Meta:
        model = Staff
        fields = [
            'user', 'Role', 'FirstName', 'LastName', 'DOB', 'Gender', 
            'BloodGroup', 'Address', 'Email', 'Contact'
        ]
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = UserCreateSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        
        staff = Staff.objects.create(user=user, **validated_data)
        return staff


class SpecializationSerializer(serializers.ModelSerializer):
    """Serializer for Specialization model"""
    doctors_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Specialization
        fields = ['id', 'SpecializationName', 'Description', 'IsActive', 'doctors_count', 'CreatedAt']
        read_only_fields = ['id', 'CreatedAt']
    
    def get_doctors_count(self, obj):
        """Get count of active doctors in this specialization"""
        return obj.doctor_set.filter(IsAvailable=True, StaffId__IsActive=True).count()


class DoctorSerializer(serializers.ModelSerializer):
    """Serializer for Doctor model with nested relationships"""
    staff = StaffSerializer(source='StaffId', read_only=True)
    staff_id = serializers.IntegerField(source='StaffId.id', write_only=True)
    specialization = SpecializationSerializer(source='SpecializationId', read_only=True)
    specialization_id = serializers.IntegerField(source='SpecializationId.id', write_only=True)
    doctor_name = serializers.SerializerMethodField()
    consultation_days_display = serializers.SerializerMethodField()
    
    class Meta:
        model = Doctor
        fields = [
            'DoctorId', 'staff', 'staff_id', 'specialization', 'specialization_id',
            'doctor_name', 'ConsultationFee', 'ConsultationDays', 'consultation_days_display', 
            'ConsultationTime', 'YearsOfExperience', 'IsAvailable', 'CreatedAt', 'UpdatedAt'
        ]
        read_only_fields = ['DoctorId', 'CreatedAt', 'UpdatedAt']
    
    def get_doctor_name(self, obj):
        """Get formatted doctor name"""
        if obj.StaffId:
            return f"Dr. {obj.StaffId.FirstName} {obj.StaffId.LastName}"
        return None
    
    def get_consultation_days_display(self, obj):
        """Get human-readable consultation days"""
        return obj.get_consultation_days_display()
    
    def validate_staff_id(self, value):
        """Validate staff member exists and has doctor role"""
        try:
            staff = Staff.objects.get(id=value)
        except Staff.DoesNotExist:
            raise serializers.ValidationError("Staff member does not exist")
        
        if staff.Role != Staff.RoleChoices.DOCTOR:
            raise serializers.ValidationError("Staff member must have Doctor role")
        
        # Check if doctor profile already exists for this staff
        if Doctor.objects.filter(StaffId=staff).exists():
            raise serializers.ValidationError("Doctor profile already exists for this staff member")
        
        return value
    
    def validate_specialization_id(self, value):
        """Validate specialization exists and is active"""
        try:
            specialization = Specialization.objects.get(id=value)
        except Specialization.DoesNotExist:
            raise serializers.ValidationError("Specialization does not exist")
        
        if not specialization.IsActive:
            raise serializers.ValidationError("Selected specialization is not active")
        
        return value


class DoctorListSerializer(serializers.ModelSerializer):
    """Simplified serializer for doctor list views"""
    staff_id = serializers.CharField(source='StaffId.StaffId', read_only=True)
    doctor_name = serializers.SerializerMethodField()
    specialization_name = serializers.CharField(source='SpecializationId.SpecializationName', read_only=True)
    
    class Meta:
        model = Doctor
        fields = [
            'DoctorId', 'staff_id', 'doctor_name', 'specialization_name',
            'ConsultationFee', 'ConsultationDays', 'ConsultationTime',
            'YearsOfExperience', 'IsAvailable'
        ]
    
    def get_doctor_name(self, obj):
        if obj.StaffId:
            return f"Dr. {obj.StaffId.FirstName} {obj.StaffId.LastName}"
        return None


class StaffSummarySerializer(serializers.ModelSerializer):
    """Summary serializer for staff (used in reports)"""
    role_display = serializers.CharField(source='get_Role_display', read_only=True)
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Staff
        fields = ['StaffId', 'full_name', 'Role', 'role_display', 'Email', 'Contact', 'IsActive']
    
    def get_full_name(self, obj):
        return f"{obj.FirstName} {obj.LastName}"