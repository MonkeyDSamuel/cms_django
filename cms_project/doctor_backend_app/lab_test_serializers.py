from rest_framework import serializers
from .models import LabTest

class LabTestSerializer(serializers.ModelSerializer):
    """Serializer for LabTest model"""
    
    class Meta:
        model = LabTest
        fields = [
            'id', 'test_name', 'test_type', 'test_instructions', 
            'test_fasting_required', 'is_active', 'Created_At', 'Updated_At'
        ]
        read_only_fields = ['id', 'Created_At', 'Updated_At']

