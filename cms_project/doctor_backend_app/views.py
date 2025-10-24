from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .models import Consultation, MedicinePrescription, LabPrescription
from .serializers import ConsultationSerializer, MedicinePrescriptionSerializer, LabPrescriptionSerializer
from receptionist_backend_app.models import Appointment


class ConsultationListCreateView(generics.ListCreateAPIView):
    """View for listing and creating consultations (GET and POST only)"""
    queryset = Consultation.objects.all()
    serializer_class = ConsultationSerializer
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        """GET method to retrieve all consultations"""
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        """POST method to create a new consultation"""
        return super().post(request, *args, **kwargs)


class MedicinePrescriptionListCreateView(generics.ListCreateAPIView):
    """View for listing and creating medicine prescriptions (GET and POST only)"""
    queryset = MedicinePrescription.objects.all()
    serializer_class = MedicinePrescriptionSerializer
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        """GET method to retrieve all medicine prescriptions"""
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        """POST method to create a new medicine prescription"""
        return super().post(request, *args, **kwargs)


class LabPrescriptionListCreateView(generics.ListCreateAPIView):
    """View for listing and creating lab prescriptions (GET and POST only)"""
    queryset = LabPrescription.objects.all()
    serializer_class = LabPrescriptionSerializer
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        """GET method to retrieve all lab prescriptions"""
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        """POST method to create a new lab prescription"""
        return super().post(request, *args, **kwargs)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def start_consultation(request):
    """Start a consultation for an appointment"""
    try:
        appointment_id = request.data.get('appointment_id')
        
        if not appointment_id:
            return Response({
                'success': False,
                'message': 'Appointment ID is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Get the appointment
        try:
            appointment = Appointment.objects.get(id=appointment_id)
        except Appointment.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Appointment not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Check if consultation already exists
        if Consultation.objects.filter(AppointmentId=appointment).exists():
            return Response({
                'success': False,
                'message': 'Consultation already exists for this appointment'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create consultation
        consultation = Consultation.objects.create(AppointmentId=appointment)
        
        # Update appointment status to IN_PROGRESS
        appointment.Status = 'IN_PROGRESS'
        appointment.save()
        
        # Serialize the consultation
        serializer = ConsultationSerializer(consultation)
        
        return Response({
            'success': True,
            'message': 'Consultation started successfully',
            'consultation': serializer.data
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({
            'success': False,
            'message': f'Error starting consultation: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_consultation_status(request, consultation_id):
    """Update consultation status"""
    try:
        consultation = Consultation.objects.get(id=consultation_id)
        new_status = request.data.get('status')
        
        if not new_status:
            return Response({
                'success': False,
                'message': 'Status is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate status
        valid_statuses = [choice[0] for choice in Consultation.StatusChoices.choices]
        if new_status not in valid_statuses:
            return Response({
                'success': False,
                'message': f'Invalid status. Valid options: {valid_statuses}'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Update consultation status
        consultation.Status = new_status
        consultation.save()
        
        # Update appointment status to match consultation status
        if new_status == 'COMPLETED':
            consultation.AppointmentId.Status = 'COMPLETED'
        elif new_status == 'CANCELLED':
            consultation.AppointmentId.Status = 'CANCELLED'
        elif new_status == 'ON_HOLD':
            consultation.AppointmentId.Status = 'ON_HOLD'
        elif new_status == 'IN_PROGRESS':
            consultation.AppointmentId.Status = 'IN_PROGRESS'
        
        consultation.AppointmentId.save()
        
        serializer = ConsultationSerializer(consultation)
        
        return Response({
            'success': True,
            'message': 'Consultation status updated successfully',
            'consultation': serializer.data
        }, status=status.HTTP_200_OK)
        
    except Consultation.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Consultation not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'success': False,
            'message': f'Error updating consultation status: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_consultation_notes(request, consultation_id):
    """Update consultation notes"""
    try:
        consultation = Consultation.objects.get(id=consultation_id)
        notes = request.data.get('notes', '')
        
        # Update consultation notes
        consultation.Notes = notes
        consultation.save()
        
        serializer = ConsultationSerializer(consultation)
        
        return Response({
            'success': True,
            'message': 'Consultation notes updated successfully',
            'consultation': serializer.data
        }, status=status.HTTP_200_OK)
        
    except Consultation.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Consultation not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'success': False,
            'message': f'Error updating consultation notes: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


