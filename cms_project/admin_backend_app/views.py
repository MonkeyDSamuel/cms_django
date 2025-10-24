from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.db import transaction
from django.utils import timezone
from .models import Staff, Doctor, Specialization
from .permissions import IsAdminOrStaffAdmin
from .serializers import StaffSerializer, DoctorSerializer, SpecializationSerializer
import json


@api_view(['GET'])
@permission_classes([IsAdminOrStaffAdmin])
def get_all_staff(request):
    """Get all staff members"""
    try:
        staff_members = Staff.objects.filter(IsActive=True).order_by('-CreatedAt')
        serializer = StaffSerializer(staff_members, many=True)
        return Response({
            'success': True,
            'data': serializer.data
        })
    except Exception as e:
        return Response({
            'success': False,
            'error': f'Failed to retrieve staff members: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAdminOrStaffAdmin])
def get_staff_by_id(request, staff_id):
    """Get specific staff member by ID"""
    try:
        staff = Staff.objects.get(id=staff_id, IsActive=True)
        serializer = StaffSerializer(staff)
        return Response({
            'success': True,
            'data': serializer.data
        })
    except Staff.DoesNotExist:
        return Response({
            'success': False,
            'error': 'Staff member not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'success': False,
            'error': f'Failed to retrieve staff member: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAdminOrStaffAdmin])
def add_staff(request):
    """Add a new staff member with user account"""
    try:
        with transaction.atomic():
            # Extract user data and staff data
            user_data = request.data.get('user', {})
            staff_data = request.data.copy()
            staff_data.pop('user', None)
            
            # Create user account
            username = user_data.get('username')
            password = user_data.get('password')
            email = user_data.get('email', '')
            first_name = user_data.get('first_name', '')
            last_name = user_data.get('last_name', '')
            
            if not username or not password:
                return Response({
                    'success': False,
                    'error': 'Username and password are required'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Check if username already exists
            if User.objects.filter(username=username).exists():
                return Response({
                    'success': False,
                    'error': 'Username already exists'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Prevent creating admin staff members through this endpoint
            role = staff_data.get('Role')
            if role == 'ADMIN':
                return Response({
                    'success': False,
                    'error': 'Admin users cannot be created through staff creation endpoint. Please use the authentication system to create admin users.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Create user
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name
            )
            
            # Create staff member
            staff = Staff.objects.create(
                user=user,
                Role=staff_data.get('Role'),
                FirstName=staff_data.get('FirstName'),
                LastName=staff_data.get('LastName'),
                DOB=staff_data.get('DOB'),
                Gender=staff_data.get('Gender'),
                BloodGroup=staff_data.get('BloodGroup'),
                Address=staff_data.get('Address'),
                Email=staff_data.get('Email'),
                Contact=staff_data.get('Contact')
            )
            
            # Return response with username, password, and role
            return Response({
                'success': True,
                'message': 'Staff member created successfully',
                'data': {
                    'staff_id': staff.id,
                    'staff_staff_id': staff.StaffId,
                    'username': username,
                    'password': password,
                    'role': staff.Role,
                    'role_display': staff.get_Role_display(),
                    'full_name': f"{staff.FirstName} {staff.LastName}",
                    'email': staff.Email
                }
            }, status=status.HTTP_201_CREATED)
            
    except Exception as e:
        return Response({
            'success': False,
            'error': f'Failed to create staff member: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAdminOrStaffAdmin])
def update_staff(request):
    """Update staff member details"""
    try:
        staff_id = request.data.get('staff_id')
        if not staff_id:
            return Response({
                'success': False,
                'error': 'staff_id is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        staff = Staff.objects.get(id=staff_id)
        
        # Prevent changing role to ADMIN
        new_role = request.data.get('Role')
        if new_role == 'ADMIN':
            return Response({
                'success': False,
                'error': 'Cannot change staff role to ADMIN. Admin users must be created through the authentication system.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Update staff fields
        if 'Role' in request.data:
            staff.Role = request.data['Role']
        if 'FirstName' in request.data:
            staff.FirstName = request.data['FirstName']
        if 'LastName' in request.data:
            staff.LastName = request.data['LastName']
        if 'DOB' in request.data:
            staff.DOB = request.data['DOB']
        if 'Gender' in request.data:
            staff.Gender = request.data['Gender']
        if 'BloodGroup' in request.data:
            staff.BloodGroup = request.data['BloodGroup']
        if 'Address' in request.data:
            staff.Address = request.data['Address']
        if 'Email' in request.data:
            staff.Email = request.data['Email']
        if 'Contact' in request.data:
            staff.Contact = request.data['Contact']
        
        staff.UpdatedAt = timezone.now()
        staff.save()
        
        # Update user account if provided
        if 'user' in request.data:
            user_data = request.data['user']
            user = staff.user
            if 'email' in user_data:
                user.email = user_data['email']
            if 'first_name' in user_data:
                user.first_name = user_data['first_name']
            if 'last_name' in user_data:
                user.last_name = user_data['last_name']
            user.save()
        
        # If role is DOC, also update doctor profile if it exists
        if staff.Role == 'DOC':
            try:
                doctor = Doctor.objects.get(Staff=staff)
                if 'FirstName' in request.data:
                    doctor.FirstName = request.data['FirstName']
                if 'LastName' in request.data:
                    doctor.LastName = request.data['LastName']
                if 'DOB' in request.data:
                    doctor.DOB = request.data['DOB']
                if 'Gender' in request.data:
                    doctor.Gender = request.data['Gender']
                if 'BloodGroup' in request.data:
                    doctor.BloodGroup = request.data['BloodGroup']
                if 'Address' in request.data:
                    doctor.Address = request.data['Address']
                if 'Email' in request.data:
                    doctor.Email = request.data['Email']
                if 'Contact' in request.data:
                    doctor.Contact = request.data['Contact']
                
                doctor.UpdatedAt = timezone.now()
                doctor.save()
            except Doctor.DoesNotExist:
                pass  # Doctor profile doesn't exist, skip doctor update
        
        return Response({
            'success': True,
            'message': 'Staff information updated successfully',
            'data': {
                'staff_id': staff.StaffId,
                'updated_at': staff.UpdatedAt
            }
        })
        
    except Staff.DoesNotExist:
        return Response({
            'success': False,
            'error': 'Staff member not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'success': False,
            'error': f'Failed to update staff member: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAdminOrStaffAdmin])
def deactivate_staff(request):
    """Deactivate staff member (set IsActive to false)"""
    try:
        staff_id = request.data.get('staff_id')
        if not staff_id:
            return Response({
                'success': False,
                'error': 'staff_id is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        staff = Staff.objects.get(id=staff_id)
        staff.IsActive = False
        staff.UpdatedAt = timezone.now()
        staff.save()
        return Response({
            'success': True,
            'message': f'Staff member {staff.StaffId} has been deactivated',
            'data': {
                'staff_id': staff.StaffId,
                'is_active': staff.IsActive
            }
        })
        
    except Staff.DoesNotExist:
        return Response({
            'success': False,
            'error': 'Staff member not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'success': False,
            'error': f'Failed to deactivate staff member: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)


# Doctor Views
@api_view(['GET'])
@permission_classes([IsAdminOrStaffAdmin])
def get_all_doctors(request):
    """Get all doctors"""
    try:
        doctors = Doctor.objects.filter(IsActive=True).order_by('-CreatedAt')
        serializer = DoctorSerializer(doctors, many=True)
        return Response({
            'success': True,
            'data': serializer.data
        })
    except Exception as e:
        return Response({
            'success': False,
            'error': f'Failed to retrieve doctors: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAdminOrStaffAdmin])
def get_doctor_by_id(request, doctor_id):
    """Get specific doctor by ID"""
    try:
        doctor = Doctor.objects.get(id=doctor_id, IsActive=True)
        serializer = DoctorSerializer(doctor)
        return Response({
            'success': True,
            'data': serializer.data
        })
    except Doctor.DoesNotExist:
        return Response({
            'success': False,
            'error': 'Doctor not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'success': False,
            'error': f'Failed to retrieve doctor: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAdminOrStaffAdmin])
def create_doctor(request):
    """Create a new doctor profile"""
    try:
        staff_id = request.data.get('staff_id')
        if not staff_id:
            return Response({
                'success': False,
                'error': 'staff_id is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if staff exists and has DOC role
        try:
            staff = Staff.objects.get(id=staff_id, Role='DOC', IsActive=True)
        except Staff.DoesNotExist:
            return Response({
                'success': False,
                'error': 'Staff member not found or not a doctor'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Check if doctor profile already exists
        if Doctor.objects.filter(Staff=staff).exists():
            return Response({
                'success': False,
                'error': 'Doctor profile already exists for this staff member'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create doctor profile
        doctor = Doctor.objects.create(
            Staff=staff,
            FirstName=request.data.get('FirstName', staff.FirstName),
            LastName=request.data.get('LastName', staff.LastName),
            DOB=request.data.get('DOB', staff.DOB),
            Gender=request.data.get('Gender', staff.Gender),
            BloodGroup=request.data.get('BloodGroup', staff.BloodGroup),
            Address=request.data.get('Address', staff.Address),
            Email=request.data.get('Email', staff.Email),
            Contact=request.data.get('Contact', staff.Contact),
            Specialization=request.data.get('Specialization', ''),
            Qualification=request.data.get('Qualification', ''),
            Experience=request.data.get('Experience', 0),
            ConsultationFee=request.data.get('ConsultationFee', 0.0)
        )
        
        return Response({
            'success': True,
            'message': 'Doctor profile created successfully',
            'data': {
                'doctor_id': doctor.id,
                'doctor_staff_id': doctor.DoctorId,
                'staff_id': staff.StaffId,
                'full_name': f"{doctor.FirstName} {doctor.LastName}",
                'specialization': doctor.Specialization,
                'qualification': doctor.Qualification,
                'experience': doctor.Experience,
                'consultation_fee': doctor.ConsultationFee
            }
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({
            'success': False,
            'error': f'Failed to create doctor profile: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAdminOrStaffAdmin])
def update_doctor(request):
    """Update doctor profile"""
    try:
        doctor_id = request.data.get('doctor_id')
        if not doctor_id:
            return Response({
                'success': False,
                'error': 'doctor_id is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        doctor = Doctor.objects.get(id=doctor_id)
        
        # Update doctor fields
        if 'FirstName' in request.data:
            doctor.FirstName = request.data['FirstName']
        if 'LastName' in request.data:
            doctor.LastName = request.data['LastName']
        if 'DOB' in request.data:
            doctor.DOB = request.data['DOB']
        if 'Gender' in request.data:
            doctor.Gender = request.data['Gender']
        if 'BloodGroup' in request.data:
            doctor.BloodGroup = request.data['BloodGroup']
        if 'Address' in request.data:
            doctor.Address = request.data['Address']
        if 'Email' in request.data:
            doctor.Email = request.data['Email']
        if 'Contact' in request.data:
            doctor.Contact = request.data['Contact']
        if 'Specialization' in request.data:
            doctor.Specialization = request.data['Specialization']
        if 'Qualification' in request.data:
            doctor.Qualification = request.data['Qualification']
        if 'Experience' in request.data:
            doctor.Experience = request.data['Experience']
        if 'ConsultationFee' in request.data:
            doctor.ConsultationFee = request.data['ConsultationFee']
        
        doctor.UpdatedAt = timezone.now()
        doctor.save()
        
        return Response({
            'success': True,
            'message': 'Doctor profile updated successfully',
            'data': {
                'doctor_id': doctor.DoctorId,
                'updated_at': doctor.UpdatedAt
            }
        })
        
    except Doctor.DoesNotExist:
        return Response({
            'success': False,
            'error': 'Doctor not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'success': False,
            'error': f'Failed to update doctor: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)


# Specialization Views
@api_view(['GET'])
@permission_classes([IsAdminOrStaffAdmin])
def get_all_specializations(request):
    """Get all specializations"""
    try:
        specializations = Specialization.objects.filter(IsActive=True).order_by('SpecializationName')
        serializer = SpecializationSerializer(specializations, many=True)
        return Response({
            'success': True,
            'data': serializer.data
        })
    except Exception as e:
        return Response({
            'success': False,
            'error': f'Failed to retrieve specializations: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAdminOrStaffAdmin])
def add_specialization(request):
    """Add a new specialization"""
    try:
        name = request.data.get('SpecializationName')
        description = request.data.get('Description', '')
        
        if not name:
            return Response({
                'success': False,
                'error': 'Specialization name is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if specialization already exists
        if Specialization.objects.filter(SpecializationName=name, IsActive=True).exists():
            return Response({
                'success': False,
                'error': 'Specialization already exists'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        specialization = Specialization.objects.create(
            SpecializationName=name,
            Description=description
        )
        
        return Response({
            'success': True,
            'message': 'Specialization added successfully',
            'data': {
                'specialization_id': specialization.id,
                'name': specialization.SpecializationName,
                'description': specialization.Description
            }
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({
            'success': False,
            'error': f'Failed to add specialization: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)