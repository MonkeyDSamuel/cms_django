from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db import transaction
from django.core.exceptions import ValidationError
import json
from .models import Staff, Doctor, Specialization


# ==================== STAFF VIEWS ====================

@csrf_exempt
def get_all_staff(request):
    """Get all staff members"""
    if request.method != 'GET':
        return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)
    
    try:
        staff_members = Staff.objects.filter(IsActive=True).select_related('user')
        staff_data = []
        
        for staff in staff_members:
            staff_data.append({
                'id': staff.id,
                'staff_id': staff.StaffId,
                'username': staff.user.username,
                'role': staff.Role,
                'role_display': staff.get_Role_display(),
                'first_name': staff.FirstName,
                'last_name': staff.LastName,
                'full_name': f"{staff.FirstName} {staff.LastName}",
                'email': staff.Email,
                'contact': staff.Contact,
                'dob': staff.DOB.strftime('%Y-%m-%d'),
                'gender': staff.Gender,
                'blood_group': staff.BloodGroup,
                'address': staff.Address,
                'is_active': staff.IsActive,
                'created_at': staff.CreatedAt.strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at': staff.UpdatedAt.strftime('%Y-%m-%d %H:%M:%S')
            })
        
        return JsonResponse({
            'success': True,
            'data': staff_data,
            'count': len(staff_data)
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error retrieving staff: {str(e)}'
        }, status=500)


@csrf_exempt
def get_staff_by_id(request, staff_id):
    """Get specific staff member by ID"""
    if request.method != 'GET':
        return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)
    
    try:
        staff = Staff.objects.select_related('user').get(id=staff_id, IsActive=True)
        
        staff_data = {
            'id': staff.id,
            'staff_id': staff.StaffId,
            'username': staff.user.username,
            'role': staff.Role,
            'role_display': staff.get_Role_display(),
            'first_name': staff.FirstName,
            'last_name': staff.LastName,
            'full_name': f"{staff.FirstName} {staff.LastName}",
            'email': staff.Email,
            'contact': staff.Contact,
            'dob': staff.DOB.strftime('%Y-%m-%d'),
            'gender': staff.Gender,
            'blood_group': staff.BloodGroup,
            'address': staff.Address,
            'is_active': staff.IsActive,
            'created_at': staff.CreatedAt.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': staff.UpdatedAt.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return JsonResponse({
            'success': True,
            'data': staff_data
        })
    
    except Staff.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Staff member not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error retrieving staff: {str(e)}'
        }, status=500)


@csrf_exempt
def add_staff(request):
    """Add new staff member with user account"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        
        # Validate required fields
        required_fields = ['user', 'Role', 'FirstName', 'LastName', 'DOB', 'Gender', 'BloodGroup', 'Address', 'Email', 'Contact']
        for field in required_fields:
            if field not in data:
                return JsonResponse({
                    'success': False,
                    'message': f'Missing required field: {field}'
                }, status=400)
        
        user_data = data['user']
        user_required_fields = ['username', 'password', 'email', 'first_name', 'last_name']
        for field in user_required_fields:
            if field not in user_data:
                return JsonResponse({
                    'success': False,
                    'message': f'Missing required user field: {field}'
                }, status=400)
        
        with transaction.atomic():
            # Create user account
            user = User.objects.create_user(
                username=user_data['username'],
                password=user_data['password'],
                email=user_data['email'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name']
            )
            
            # Create staff member
            staff = Staff.objects.create(
                user=user,
                Role=data['Role'],
                FirstName=data['FirstName'],
                LastName=data['LastName'],
                DOB=data['DOB'],
                Gender=data['Gender'],
                BloodGroup=data['BloodGroup'],
                Address=data['Address'],
                Email=data['Email'],
                Contact=data['Contact']
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Staff member created successfully',
                'data': {
                    'staff_id': staff.id,
                    'staff_staff_id': staff.StaffId,
                    'username': user.username,
                    'password': user_data['password'],
                    'role': staff.Role,
                    'role_display': staff.get_Role_display(),
                    'full_name': f"{staff.FirstName} {staff.LastName}",
                    'email': staff.Email
                }
            })
    
    except ValidationError as e:
        return JsonResponse({
            'success': False,
            'message': f'Validation error: {str(e)}'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error creating staff: {str(e)}'
        }, status=500)


@csrf_exempt
def update_staff(request):
    """Update staff member details"""
    if request.method != 'PUT':
        return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        
        if 'staff_id' not in data:
            return JsonResponse({
                'success': False,
                'message': 'staff_id is required'
            }, status=400)
        
        staff = Staff.objects.get(id=data['staff_id'], IsActive=True)
        
        # Update staff fields
        updatable_fields = ['FirstName', 'LastName', 'DOB', 'Gender', 'BloodGroup', 'Address', 'Email', 'Contact']
        for field in updatable_fields:
            if field in data:
                setattr(staff, field, data[field])
        
        # Update user password if provided
        if 'Password' in data and data['Password']:
            user = staff.user
            user.set_password(data['Password'])
            user.save()
        
        staff.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Staff member updated successfully',
            'data': {
                'staff_id': staff.id,
                'staff_staff_id': staff.StaffId,
                'full_name': f"{staff.FirstName} {staff.LastName}",
                'email': staff.Email,
                'updated_at': staff.UpdatedAt.strftime('%Y-%m-%d %H:%M:%S')
            }
        })
    
    except Staff.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Staff member not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error updating staff: {str(e)}'
        }, status=500)


@csrf_exempt
def deactivate_staff(request):
    """Deactivate staff member (set IsActive to false)"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        
        if 'staff_id' not in data:
            return JsonResponse({
                'success': False,
                'message': 'staff_id is required'
            }, status=400)
        
        staff = Staff.objects.get(id=data['staff_id'], IsActive=True)
        staff.IsActive = False
        staff.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Staff member deactivated successfully',
            'data': {
                'staff_id': staff.id,
                'staff_staff_id': staff.StaffId,
                'full_name': f"{staff.FirstName} {staff.LastName}",
                'is_active': staff.IsActive
            }
        })
    
    except Staff.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Staff member not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error deactivating staff: {str(e)}'
        }, status=500)


# ==================== DOCTOR VIEWS ====================

@csrf_exempt
def get_all_doctors(request):
    """Get all doctors"""
    if request.method != 'GET':
        return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)
    
    try:
        doctors = Doctor.objects.select_related('StaffId__user', 'SpecializationId').filter(StaffId__IsActive=True)
        doctor_data = []
        
        for doctor in doctors:
            doctor_data.append({
                'doctor_id': doctor.DoctorId,
                'staff_id': doctor.StaffId.id,
                'staff_staff_id': doctor.StaffId.StaffId,
                'username': doctor.StaffId.user.username,
                'full_name': f"Dr. {doctor.StaffId.FirstName} {doctor.StaffId.LastName}",
                'specialization': doctor.SpecializationId.SpecializationName,
                'specialization_id': doctor.SpecializationId.id,
                'consultation_fee': float(doctor.ConsultationFee),
                'consultation_days': doctor.ConsultationDays,
                'consultation_time': doctor.ConsultationTime,
                'years_of_experience': doctor.YearsOfExperience,
                'is_available': doctor.IsAvailable,
                'email': doctor.StaffId.Email,
                'contact': doctor.StaffId.Contact,
                'created_at': doctor.CreatedAt.strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at': doctor.UpdatedAt.strftime('%Y-%m-%d %H:%M:%S')
            })
        
        return JsonResponse({
            'success': True,
            'data': doctor_data,
            'count': len(doctor_data)
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error retrieving doctors: {str(e)}'
        }, status=500)


@csrf_exempt
def get_doctor_by_id(request, doctor_id):
    """Get specific doctor by ID"""
    if request.method != 'GET':
        return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)
    
    try:
        doctor = Doctor.objects.select_related('StaffId__user', 'SpecializationId').get(DoctorId=doctor_id, StaffId__IsActive=True)
        
        doctor_data = {
            'doctor_id': doctor.DoctorId,
            'staff_id': doctor.StaffId.id,
            'staff_staff_id': doctor.StaffId.StaffId,
            'username': doctor.StaffId.user.username,
            'full_name': f"Dr. {doctor.StaffId.FirstName} {doctor.StaffId.LastName}",
            'specialization': doctor.SpecializationId.SpecializationName,
            'specialization_id': doctor.SpecializationId.id,
            'consultation_fee': float(doctor.ConsultationFee),
            'consultation_days': doctor.ConsultationDays,
            'consultation_time': doctor.ConsultationTime,
            'years_of_experience': doctor.YearsOfExperience,
            'is_available': doctor.IsAvailable,
            'email': doctor.StaffId.Email,
            'contact': doctor.StaffId.Contact,
            'created_at': doctor.CreatedAt.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': doctor.UpdatedAt.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return JsonResponse({
            'success': True,
            'data': doctor_data
        })
    
    except Doctor.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Doctor not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error retrieving doctor: {str(e)}'
        }, status=500)


@csrf_exempt
def get_doctor_by_staff_id(request, staff_id):
    """Get doctor by staff ID"""
    if request.method != 'GET':
        return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)
    
    try:
        doctor = Doctor.objects.select_related('StaffId__user', 'SpecializationId').get(StaffId__id=staff_id, StaffId__IsActive=True)
        
        doctor_data = {
            'doctor_id': doctor.DoctorId,
            'staff_id': doctor.StaffId.id,
            'staff_staff_id': doctor.StaffId.StaffId,
            'username': doctor.StaffId.user.username,
            'full_name': f"Dr. {doctor.StaffId.FirstName} {doctor.StaffId.LastName}",
            'specialization': doctor.SpecializationId.SpecializationName,
            'specialization_id': doctor.SpecializationId.id,
            'consultation_fee': float(doctor.ConsultationFee),
            'consultation_days': doctor.ConsultationDays,
            'consultation_time': doctor.ConsultationTime,
            'years_of_experience': doctor.YearsOfExperience,
            'is_available': doctor.IsAvailable,
            'email': doctor.StaffId.Email,
            'contact': doctor.StaffId.Contact,
            'created_at': doctor.CreatedAt.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': doctor.UpdatedAt.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return JsonResponse({
            'success': True,
            'data': doctor_data
        })
    
    except Doctor.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Doctor profile not found for this staff member'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error retrieving doctor: {str(e)}'
        }, status=500)


@csrf_exempt
def create_doctor(request):
    """Create new doctor profile"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        
        # Validate required fields
        required_fields = ['staff_id', 'specialization_id', 'consultation_fee', 'consultation_days', 'consultation_time', 'years_of_experience']
        for field in required_fields:
            if field not in data:
                return JsonResponse({
                    'success': False,
                    'message': f'Missing required field: {field}'
                }, status=400)
        
        # Check if staff member exists and is a doctor
        staff = Staff.objects.get(id=data['staff_id'], Role=Staff.RoleChoices.DOCTOR, IsActive=True)
        
        # Check if doctor profile already exists
        if Doctor.objects.filter(StaffId=staff).exists():
            return JsonResponse({
                'success': False,
                'message': 'Doctor profile already exists for this staff member'
            }, status=400)
        
        # Check if specialization exists
        specialization = Specialization.objects.get(id=data['specialization_id'], IsActive=True)
        
        # Create doctor profile
        doctor = Doctor.objects.create(
            StaffId=staff,
            SpecializationId=specialization,
            ConsultationFee=data['consultation_fee'],
            ConsultationDays=data['consultation_days'],
            ConsultationTime=data['consultation_time'],
            YearsOfExperience=data['years_of_experience'],
            IsAvailable=data.get('is_available', True)
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Doctor profile created successfully',
            'data': {
                'doctor_id': doctor.DoctorId,
                'staff_id': staff.id,
                'staff_staff_id': staff.StaffId,
                'full_name': f"Dr. {staff.FirstName} {staff.LastName}",
                'specialization': specialization.SpecializationName,
                'consultation_fee': float(doctor.ConsultationFee),
                'years_of_experience': doctor.YearsOfExperience,
                'is_available': doctor.IsAvailable
            }
        })
    
    except Staff.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Staff member not found or not a doctor'
        }, status=404)
    except Specialization.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Specialization not found'
        }, status=404)
    except ValidationError as e:
        return JsonResponse({
            'success': False,
            'message': f'Validation error: {str(e)}'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error creating doctor: {str(e)}'
        }, status=500)


@csrf_exempt
def update_doctor(request):
    """Update doctor details"""
    if request.method != 'PUT':
        return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        
        if 'doctor_id' not in data:
            return JsonResponse({
                'success': False,
                'message': 'doctor_id is required'
            }, status=400)
        
        doctor = Doctor.objects.select_related('StaffId', 'SpecializationId').get(DoctorId=data['doctor_id'], StaffId__IsActive=True)
        
        # Update doctor fields
        updatable_fields = ['consultation_fee', 'consultation_days', 'consultation_time', 'years_of_experience', 'is_available']
        for field in updatable_fields:
            if field in data:
                setattr(doctor, field, data[field])
        
        # Update specialization if provided
        if 'specialization_id' in data:
            specialization = Specialization.objects.get(id=data['specialization_id'], IsActive=True)
            doctor.SpecializationId = specialization
        
        doctor.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Doctor profile updated successfully',
            'data': {
                'doctor_id': doctor.DoctorId,
                'staff_id': doctor.StaffId.id,
                'full_name': f"Dr. {doctor.StaffId.FirstName} {doctor.StaffId.LastName}",
                'specialization': doctor.SpecializationId.SpecializationName,
                'consultation_fee': float(doctor.ConsultationFee),
                'years_of_experience': doctor.YearsOfExperience,
                'is_available': doctor.IsAvailable,
                'updated_at': doctor.UpdatedAt.strftime('%Y-%m-%d %H:%M:%S')
            }
        })
    
    except Doctor.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Doctor not found'
        }, status=404)
    except Specialization.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Specialization not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error updating doctor: {str(e)}'
        }, status=500)


# ==================== SPECIALIZATION VIEWS ====================

@csrf_exempt
def get_all_specializations(request):
    """Get all specializations"""
    if request.method != 'GET':
        return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)
    
    try:
        specializations = Specialization.objects.filter(IsActive=True)
        specialization_data = []
        
        for spec in specializations:
            specialization_data.append({
                'id': spec.id,
                'name': spec.SpecializationName,
                'description': spec.Description,
                'is_active': spec.IsActive,
                'created_at': spec.CreatedAt.strftime('%Y-%m-%d %H:%M:%S')
            })
        
        return JsonResponse({
            'success': True,
            'data': specialization_data,
            'count': len(specialization_data)
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error retrieving specializations: {str(e)}'
        }, status=500)


@csrf_exempt
def add_specialization(request):
    """Add new specialization"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        
        # Validate required fields
        required_fields = ['name', 'description']
        for field in required_fields:
            if field not in data:
                return JsonResponse({
                    'success': False,
                    'message': f'Missing required field: {field}'
                }, status=400)
        
        # Create specialization
        specialization = Specialization.objects.create(
            SpecializationName=data['name'],
            Description=data['description'],
            IsActive=data.get('is_active', True)
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Specialization added successfully',
            'data': {
                'id': specialization.id,
                'name': specialization.SpecializationName,
                'description': specialization.Description,
                'is_active': specialization.IsActive,
                'created_at': specialization.CreatedAt.strftime('%Y-%m-%d %H:%M:%S')
            }
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error adding specialization: {str(e)}'
        }, status=500)

