from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Category, Test, Prescription, LabTestResult, LabBilling, BillingItem
from .serializers import (
    CategorySerializer, TestSerializer, PrescriptionSerializer, 
    LabTestResultSerializer, LabBillingSerializer, BillingItemSerializer
)
from .permissions import IsLabTechnician

# ----------------------------
# Category ViewSet
# ----------------------------
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsLabTechnician]


# ----------------------------
# Test ViewSet
# ----------------------------
class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    permission_classes = [IsLabTechnician]

    @action(detail=False, methods=['get'])
    def get_tests_by_category(self, request, cat_id=None):
        tests = Test.objects.filter(category_id=cat_id, is_active=True)
        serializer = self.get_serializer(tests, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def search_tests(self, request):
        query = request.GET.get('q', '')
        tests = Test.objects.filter(
            Q(test_id__icontains=query) | 
            Q(test_name__icontains=query)
        )
        serializer = self.get_serializer(tests, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'])
    def toggle_status(self, request, pk=None):
        test = self.get_object()
        test.is_active = not test.is_active
        test.save()
        serializer = self.get_serializer(test)
        return Response(serializer.data)


# ----------------------------
# Prescription ViewSet (NEW)
# ----------------------------
class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    permission_classes = [IsLabTechnician]

    @action(detail=False, methods=['get'])
    def search_prescriptions(self, request):
        query = request.GET.get('q', '')
        prescriptions = Prescription.objects.filter(
            Q(patient_name__icontains=query) | 
            Q(patient_id__icontains=query) |
            Q(pres_id__icontains=query)
        )
        serializer = self.get_serializer(prescriptions, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        prescription = self.get_object()
        new_status = request.data.get('status')
        if new_status in dict(Prescription.STATUS_CHOICES):
            prescription.status = new_status
            prescription.save()
            serializer = self.get_serializer(prescription)
            return Response(serializer.data)
        return Response(
            {"error": "Invalid status"}, 
            status=status.HTTP_400_BAD_REQUEST
        )


# ----------------------------
# Lab Test Result ViewSet (UPDATED)
# ----------------------------
class LabTestResultViewSet(viewsets.ModelViewSet):
    queryset = LabTestResult.objects.all()
    serializer_class = LabTestResultSerializer
    permission_classes = [IsLabTechnician]

    @action(detail=False, methods=['get'])
    def get_results_by_prescription(self, request, pres_id=None):
        results = LabTestResult.objects.filter(prescription_id=pres_id)
        serializer = self.get_serializer(results, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        result = self.get_object()
        new_status = request.data.get('status')
        if new_status in dict(LabTestResult.STATUS_CHOICES):
            result.status = new_status
            result.save()
            serializer = self.get_serializer(result)
            return Response(serializer.data)
        return Response(
            {"error": "Invalid status"}, 
            status=status.HTTP_400_BAD_REQUEST
        )


# ----------------------------
# Lab Billing ViewSet (UPDATED)
# ----------------------------
class LabBillingViewSet(viewsets.ModelViewSet):
    queryset = LabBilling.objects.all()
    serializer_class = LabBillingSerializer
    permission_classes = [IsLabTechnician]

    @action(detail=False, methods=['get'])
    def get_bills_by_prescription(self, request, pres_id=None):
        bills = LabBilling.objects.filter(prescription_id=pres_id)
        serializer = self.get_serializer(bills, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        bill = self.get_object()
        new_status = request.data.get('status')
        if new_status in dict(LabBilling.STATUS_CHOICES):
            bill.status = new_status
            bill.save()
            serializer = self.get_serializer(bill)
            return Response(serializer.data)
        return Response(
            {"error": "Invalid status"}, 
            status=status.HTTP_400_BAD_REQUEST
        )