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
from .permissions import IsReceptionist, IsReceptionistOrAdmin, IsReceptionistOrDoctor, IsReceptionistOrDoctorReadOnly
from admin_backend_app.models import Doctor

class PatientListCreateView(generics.ListCreateAPIView):
    """View for listing all patients and creating new patients"""
    
    permission_classes = [IsReceptionistOrDoctorReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['Gender', 'IsActive']
    search_fields = ['Name', 'PatientId', 'PhoneNumber']
    ordering_fields = ['PatientId', 'Name', 'Created_At']
    ordering = ['PatientId']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PatientCreateSerializer
        return PatientSerializer
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.request.method == 'GET':
            # Allow both receptionists and doctors to view patients
            permission_classes = [IsReceptionistOrDoctor]
        else:
            # Only allow receptionists to create patients
            permission_classes = [IsReceptionist]
        
        return [permission() for permission in permission_classes]
    
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
    
    permission_classes = [IsReceptionistOrDoctor]
    serializer_class = PatientSerializer
    queryset = Patient.objects.all()
    lookup_field = 'id'

class AppointmentListCreateView(generics.ListCreateAPIView):
    """View for listing all appointments and creating new appointments"""
    
    permission_classes = [IsReceptionistOrDoctorReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['Status', 'DoctorId', 'Date']
    search_fields = ['AppointmentId']
    ordering_fields = ['AppointmentId', 'Date', 'TokenNo', 'Created_At']
    ordering = ['Date', 'TokenNo']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AppointmentCreateSerializer
        return AppointmentSerializer
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.request.method == 'GET':
            # Allow both receptionists and doctors to view appointments
            permission_classes = [IsReceptionistOrDoctor]
        else:
            # Only allow receptionists to create appointments
            permission_classes = [IsReceptionist]
        
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        queryset = Appointment.objects.select_related('DoctorId__StaffId', 'DoctorId__SpecializationId').all()
        
        # If the user is a doctor, filter to show only their appointments
        if hasattr(self.request.user, 'staff') and self.request.user.staff.Role == 'DOCTOR':
            try:
                from admin_backend_app.models import Doctor
                doctor = Doctor.objects.get(StaffId=self.request.user.staff)
                queryset = queryset.filter(DoctorId=doctor)
            except:
                # If doctor record not found, return empty queryset
                queryset = queryset.none()
        
        return queryset
    
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
    
    permission_classes = [IsReceptionistOrDoctor]
    serializer_class = AppointmentSerializer
    lookup_field = 'id'
    
    def get_queryset(self):
        queryset = Appointment.objects.select_related('DoctorId__StaffId', 'DoctorId__SpecializationId').all()
        
        # If the user is a doctor, filter to show only their appointments
        if hasattr(self.request.user, 'staff') and self.request.user.staff.Role == 'DOCTOR':
            try:
                from admin_backend_app.models import Doctor
                doctor = Doctor.objects.get(StaffId=self.request.user.staff)
                queryset = queryset.filter(DoctorId=doctor)
            except:
                # If doctor record not found, return empty queryset
                queryset = queryset.none()
        
        return queryset

class DoctorListView(generics.ListAPIView):
    """View for listing all available doctors for appointment booking"""
    
    permission_classes = [IsReceptionistOrDoctor]
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


class DoctorBySpecializationView(generics.ListAPIView):
    """View for listing doctors by specialization"""
    
    permission_classes = [IsReceptionistOrDoctor]
    
    def get(self, request, specialization_id):
        """Get available doctors for a specific specialization"""
        from admin_backend_app.models import Specialization
        
        try:
            # Get doctors with this specialization who are active and available
            doctors = Doctor.objects.filter(
                SpecializationId=specialization_id,
                IsAvailable=True,
                StaffId__IsActive=True
            ).select_related('StaffId', 'SpecializationId')
            
            doctor_data = []
            for doctor in doctors:
                doctor_data.append({
                    'DoctorId': doctor.DoctorId,
                    'id': doctor.DoctorId,
                    'FirstName': doctor.StaffId.FirstName,
                    'LastName': doctor.StaffId.LastName,
                    'first_name': doctor.StaffId.FirstName,
                    'last_name': doctor.StaffId.LastName,
                    'ConsultationFee': float(doctor.ConsultationFee),
                    'consultation_fee': float(doctor.ConsultationFee),
                    'ConsultationDays': doctor.ConsultationDays,
                    'consultation_days': doctor.ConsultationDays,
                    'ConsultationTime': doctor.ConsultationTime,
                    'consultation_time': doctor.ConsultationTime,
                    'YearsOfExperience': doctor.YearsOfExperience,
                    'years_of_experience': doctor.YearsOfExperience,
                    'IsAvailable': doctor.IsAvailable,
                    'is_active': doctor.StaffId.IsActive
                })
            
            return Response({
                'message': 'Available doctors retrieved successfully',
                'data': doctor_data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'message': f'Error retrieving doctors: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)


class DoctorAvailableDatesView(generics.RetrieveAPIView):
    """View for getting available dates for a doctor"""
    
    permission_classes = [IsReceptionistOrDoctor]
    
    def get(self, request, doctor_id):
        """Get available dates for a doctor based on consultation days and times"""
        from datetime import datetime, timedelta, time as dt_time
        from django.utils import timezone
        
        try:
            doctor = Doctor.objects.get(DoctorId=doctor_id)
            
            # Get consultation days (array of integers)
            consultation_days = doctor.ConsultationDays if isinstance(doctor.ConsultationDays, list) else []
            
            # Get consultation time
            consultation_time = doctor.ConsultationTime or ''
            
            # Parse consultation time (format: "HH:MM-HH:MM")
            start_time = None
            end_time = None
            if consultation_time and '-' in consultation_time:
                try:
                    start_str, end_str = consultation_time.split('-')
                    start_hour, start_min = map(int, start_str.strip().split(':'))
                    end_hour, end_min = map(int, end_str.strip().split(':'))
                    start_time = dt_time(start_hour, start_min)
                    end_time = dt_time(end_hour, end_min)
                except (ValueError, AttributeError):
                    pass
            
            # Generate available dates for next 30 days
            available_dates = []
            current_datetime = timezone.now()
            current_date = current_datetime.date()
            current_time = current_datetime.time()
            
            for i in range(30):  # Next 30 days
                check_date = current_date + timedelta(days=i)
                day_of_week = check_date.weekday()  # 0=Monday, 6=Sunday in Python
                
                # Map Python weekday to our system (Sunday=1, Monday=2, etc.)
                day_mapping = {0: 2, 1: 3, 2: 4, 3: 5, 4: 6, 5: 7, 6: 1}  # Mon-Sun to our system
                mapped_day = day_mapping[day_of_week]
                
                # Check if doctor is available on this day
                if mapped_day in consultation_days:
                    # If it's today, check if consultation time is still valid
                    if i == 0:
                        if start_time and end_time:
                            # Check if current time is before end time for today
                            if current_time >= end_time:
                                continue  # Skip today if consultation time has passed
                        else:
                            # If no consultation time specified, check if it's past 5 PM
                            if current_time >= dt_time(17, 0):
                                continue  # Skip today if it's past 5 PM
                    
                    # Add this date to available dates
                    available_dates.append(check_date.strftime('%Y-%m-%d'))
            
            return Response({
                'message': 'Available dates retrieved successfully',
                'data': available_dates
            }, status=status.HTTP_200_OK)
            
        except Doctor.DoesNotExist:
            return Response({
                'message': 'Doctor not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'message': f'Error retrieving available dates: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)