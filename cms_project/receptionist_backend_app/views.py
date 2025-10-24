from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Patient, Appointment
from .serializers import (
    PatientSerializer, PatientCreateSerializer,
    AppointmentSerializer, AppointmentCreateSerializer
)
from .permissions import IsReceptionist, IsReceptionistOrAdmin
from admin_backend_app.models import Doctor

class PatientListCreateView(generics.ListCreateAPIView):
    """View for listing all patients and creating new patients"""
    
    permission_classes = [IsReceptionist]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['Gender', 'IsActive']
    search_fields = ['Name', 'PatientId', 'PhoneNumber']
    ordering_fields = ['PatientId', 'Name', 'Created_At']
    ordering = ['PatientId']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PatientCreateSerializer
        return PatientSerializer
    
    def get_queryset(self):
        return Patient.objects.all()
    
    def create(self, request, *args, **kwargs):
        """Create a new patient"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            patient = serializer.save()
            # Return the full patient data with generated PatientId
            response_serializer = PatientSerializer(patient)
            return Response({
                'message': 'Patient created successfully',
                'data': response_serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PatientDetailView(generics.RetrieveAPIView):
    """View for retrieving a specific patient"""
    
    permission_classes = [IsReceptionist]
    serializer_class = PatientSerializer
    queryset = Patient.objects.all()
    lookup_field = 'id'

class AppointmentListCreateView(generics.ListCreateAPIView):
    """View for listing all appointments and creating new appointments"""
    
    permission_classes = [IsReceptionist]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['Status', 'DoctorId', 'Date']
    search_fields = ['AppointmentId']
    ordering_fields = ['AppointmentId', 'Date', 'TokenNo', 'Created_At']
    ordering = ['Date', 'TokenNo']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AppointmentCreateSerializer
        return AppointmentSerializer
    
    def get_queryset(self):
        return Appointment.objects.select_related('DoctorId__StaffId', 'DoctorId__SpecializationId').all()
    
    def create(self, request, *args, **kwargs):
        """Create a new appointment"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            appointment = serializer.save()
            # Return the full appointment data with generated AppointmentId
            response_serializer = AppointmentSerializer(appointment)
            return Response({
                'message': 'Appointment created successfully',
                'data': response_serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AppointmentDetailView(generics.RetrieveAPIView):
    """View for retrieving a specific appointment"""
    
    permission_classes = [IsReceptionist]
    serializer_class = AppointmentSerializer
    queryset = Appointment.objects.select_related('DoctorId__StaffId', 'DoctorId__SpecializationId').all()
    lookup_field = 'id'

class DoctorListView(generics.ListAPIView):
    """View for listing all available doctors for appointment booking"""
    
    permission_classes = [IsReceptionist]
    queryset = Doctor.objects.filter(IsAvailable=True).select_related('StaffId', 'SpecializationId')
    
    def list(self, request, *args, **kwargs):
        """Return simplified doctor data for appointment booking"""
        doctors = self.get_queryset()
        doctor_data = []
        
        for doctor in doctors:
            doctor_data.append({
                'id': doctor.DoctorId,
                'name': f"Dr. {doctor.StaffId.FirstName} {doctor.StaffId.LastName}",
                'specialization': doctor.SpecializationId.SpecializationName,
                'consultation_fee': float(doctor.ConsultationFee),
                'consultation_days': doctor.ConsultationDays,
                'consultation_time': doctor.ConsultationTime,
                'years_of_experience': doctor.YearsOfExperience
            })
        
        return Response({
            'message': 'Available doctors retrieved successfully',
            'data': doctor_data
        }, status=status.HTTP_200_OK)
