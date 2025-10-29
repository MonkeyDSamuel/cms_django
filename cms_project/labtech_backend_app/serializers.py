from rest_framework import serializers
from .models import Category, Test, Prescription, LabTestResult, LabBilling, BillingItem

# ----------------------------
# Category Serializer
# ----------------------------
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


# ----------------------------
# Test Serializer
# ----------------------------
class TestSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.category_name", read_only=True)

    class Meta:
        model = Test
        fields = '__all__'


# ----------------------------
# Prescription Serializer (NEW)
# ----------------------------
# ----------------------------
# Prescription Serializer (UPDATED)
# ----------------------------
class PrescriptionSerializer(serializers.ModelSerializer):
    lab_prescription_id = serializers.CharField(source='lab_prescription.labPrescriptionId', read_only=True)
    test_name = serializers.CharField(source='lab_prescription.test_name', read_only=True)
    test_type = serializers.CharField(source='lab_prescription.test_type', read_only=True)
    test_instructions = serializers.CharField(source='lab_prescription.test_instructions', read_only=True)
    fasting_required = serializers.BooleanField(source='lab_prescription.test_fasting_required', read_only=True)

    class Meta:
        model = Prescription
        fields = [
            'pres_id', 'lab_prescription', 'lab_prescription_id', 'patient_name', 
            'patient_id', 'doctor_name', 'prescription_date', 'status', 
            'created_on', 'test_name', 'test_type', 'test_instructions', 'fasting_required'
        ]


# ----------------------------
# Billing Item Serializer (NEW)
# ----------------------------
class BillingItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillingItem
        fields = '__all__'


# ----------------------------
# Lab Billing Serializer (UPDATED)
# ----------------------------
class LabBillingSerializer(serializers.ModelSerializer):
    items = BillingItemSerializer(many=True, read_only=True)  # NEW
    patient_name = serializers.CharField(read_only=True)  # Keep as read_only for safety
    patient_id = serializers.CharField(read_only=True)  # Keep as read_only for safety

    class Meta:
        model = LabBilling
        fields = '__all__'


# ----------------------------
# Lab Test Result Serializer (UPDATED)
# ----------------------------
class LabTestResultSerializer(serializers.ModelSerializer):
    test_id = serializers.CharField(source='test.test_id', read_only=True)
    test_name = serializers.CharField(source='test.test_name', read_only=True)
    rate = serializers.DecimalField(source='test.rate', max_digits=10, decimal_places=2, read_only=True)
    category_name = serializers.CharField(source='test.category.category_name', read_only=True)
    patient_name = serializers.CharField(source='prescription.patient_name', read_only=True)  # NEW
    patient_id = serializers.CharField(source='prescription.patient_id', read_only=True)  # NEW

    class Meta:
        model = LabTestResult
        fields = [
            'result_id',
            'test',
            'test_id',
            'test_name',
            'category_name',
            'rate',
            'prescription',  # UPDATED (was lab_pres_id)
            'patient_name',  # NEW
            'patient_id',    # NEW
            'status',
            'result_value',  # NEW
            'normal_range',  # NEW
            'unit',          # NEW
            'remarks',       # NEW
            'result_date',
            'created_on'     # NEW
        ]