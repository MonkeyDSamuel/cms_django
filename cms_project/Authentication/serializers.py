from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserRole


class UserSerializer(serializers.ModelSerializer):
    """Read-only serializer for Django User model"""

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'date_joined']
        read_only_fields = ['id', 'is_active', 'date_joined']


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new users with password confirmation"""
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password_confirm']

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password_confirm'):
            raise serializers.ValidationError("Passwords don't match")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm', None)
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user 


class MinimalSignupSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True, min_length=4)
    role = serializers.ChoiceField(choices=[
        ('admin', 'admin'),
        ('receptionist', 'receptionist'),
        ('doctor', 'doctor'),
        ('lab technician', 'lab technician'),
    ])

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('Username already exists')
        return value

    def create(self, validated_data):
        role_display = validated_data.pop('role')
        # Map display values to internal codes
        role_mapping = {
            'admin': 'ADMIN',
            'receptionist': 'REC',
            'doctor': 'DOC',
            'lab technician': 'LTECH'
        }
        role_code = role_mapping[role_display]
        user = User.objects.create_user(username=validated_data['username'], password=validated_data['password'])
        UserRole.objects.create(user=user, role=role_code)
        return user 