from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from admin_backend_app.models import Staff
from .serializers import UserCreateSerializer, MinimalSignupSerializer
from .models import UserRole


@api_view(['POST'])
@permission_classes([AllowAny])
def minimal_signup(request):
    """Signup with username, password, and role only."""
    serializer = MinimalSignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()

    # tokens
    token, _ = Token.objects.get_or_create(user=user)
    refresh = RefreshToken.for_user(user)
    access = refresh.access_token

    role_entry = getattr(user, 'assigned_role', None)
    role_code = role_entry.role if role_entry else None
    role_display = UserRole.RoleChoices(role_code).label if role_code else None

    return Response({
        'message': 'User created successfully',
        'user': {
            'id': user.id,
            'username': user.username,
        },
        'role': role_code,
        'role_display': role_display,
        'token': token.key,
        'access': str(access),
        'refresh': str(refresh)
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def signup_user(request):
    try:
        data = request.data
        required_fields = ['username', 'email', 'password', 'password_confirm', 'first_name', 'last_name']
        for field in required_fields:
            if field not in data or not data[field]:
                return Response({'error': f'{field} is required'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=data['username']).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=data['email']).exists():
            return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)

        # Issue JWT tokens as well
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        return Response({
            'message': 'User created successfully',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name
            },
            'token': token.key,
            'access': str(access),
            'refresh': str(refresh)
        }, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': 'Internal server error', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    try:
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        if user is None:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        if not user.is_active:
            return Response({'error': 'User account is disabled'}, status=status.HTTP_401_UNAUTHORIZED)

        token, _ = Token.objects.get_or_create(user=user)
        # Issue JWT tokens
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        staff_info = None
        redirect_module = 'default'
        role_code = None
        role_display = None
        staff_id = None
        
        # First check if user has a Staff record
        try:
            staff = Staff.objects.get(user=user)
            if not staff.IsActive:
                return Response({'error': 'Staff account is inactive'}, status=status.HTTP_401_UNAUTHORIZED)
            staff_info = {
                'staff_id': staff.StaffId,
                'role': staff.Role,
                'role_display': staff.get_Role_display(),
                'first_name': staff.FirstName,
                'last_name': staff.LastName
            }
            role_code = staff.Role
            role_display = staff.get_Role_display()
            staff_id = staff.StaffId
            role_module_map = {
                Staff.RoleChoices.ADMIN: 'admin',
                Staff.RoleChoices.DOCTOR: 'doctor',
                Staff.RoleChoices.RECEPTIONIST: 'receptionist',
                Staff.RoleChoices.PHARMACIST: 'pharmacist',
                Staff.RoleChoices.LAB_TECHNICIAN: 'labtech'
            }
            redirect_module = role_module_map.get(staff.Role, 'default')
        except Staff.DoesNotExist:
            # If no Staff record, check UserRole table
            try:
                user_role = UserRole.objects.get(user=user)
                role_code = user_role.role
                role_display = user_role.get_role_display()
                staff_id = None
                
                # Map UserRole codes to redirect modules
                role_module_map = {
                    'ADMIN': 'admin',
                    'DOC': 'doctor',
                    'REC': 'receptionist',
                    'LTECH': 'labtech'
                }
                redirect_module = role_module_map.get(user_role.role, 'default')
            except UserRole.DoesNotExist:
                # Fallback for superusers
                if user.is_superuser:
                    redirect_module = 'admin'
                    role_code = 'ADMIN'
                    role_display = 'Administrator'
                    staff_id = None

        return Response({
            'message': 'Login successful',
            'token': token.key,
            'access': str(access),
            'refresh': str(refresh),
            'role': role_code,
            'role_display': role_display,
            'staff_id': staff_id,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'is_superuser': user.is_superuser,
                'is_staff': user.is_staff
            },
            'staff_info': staff_info,
            'redirect_module': redirect_module,
            'dashboard_url': f'/{redirect_module}/dashboard/'
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': 'Internal server error', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    try:
        request.user.auth_token.delete()
        return Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)
    except Exception:
        return Response({'error': 'Error logging out'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    try:
        user = request.user
        staff_info = None
        try:
            staff = Staff.objects.get(user=user)
            staff_info = {
                'staff_id': staff.StaffId,
                'role': staff.Role,
                'role_display': staff.get_Role_display(),
                'first_name': staff.FirstName,
                'last_name': staff.LastName,
                'email': staff.Email,
                'contact': staff.Contact,
                'is_active': staff.IsActive
            }
        except Staff.DoesNotExist:
            pass
        return Response({
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'is_superuser': user.is_superuser,
                'is_staff': user.is_staff,
                'date_joined': user.date_joined
            },
            'staff_info': staff_info
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': 'Error fetching profile', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_user_role(request):
    try:
        user = request.user
        permissions = {
            'is_admin': user.is_superuser,
            'is_staff_member': False,
            'role': None,
            'can_manage_staff': user.is_superuser,
            'can_manage_doctors': user.is_superuser,
            'can_manage_patients': False,
            'can_view_reports': user.is_superuser
        }
        try:
            staff = Staff.objects.get(user=user)
            permissions.update({
                'is_staff_member': True,
                'role': staff.Role,
                'role_display': staff.get_Role_display(),
                'staff_id': staff.StaffId
            })
            if staff.Role == Staff.RoleChoices.ADMIN:
                permissions.update({
                    'is_admin': True,
                    'can_manage_staff': True,
                    'can_manage_doctors': True,
                    'can_manage_patients': True,
                    'can_view_reports': True
                })
            elif staff.Role == Staff.RoleChoices.DOCTOR:
                permissions.update({'can_manage_patients': True})
            elif staff.Role == Staff.RoleChoices.RECEPTIONIST:
                permissions.update({'can_manage_patients': True})
        except Staff.DoesNotExist:
            pass
        return Response({'user_id': user.id, 'username': user.username, 'permissions': permissions}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': 'Error checking role', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token(request):
    """Issue a new access token from a refresh token"""
    try:
        refresh_raw = request.data.get('refresh')
        if not refresh_raw:
            return Response({'error': 'refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)
        refresh = RefreshToken(refresh_raw)
        access = refresh.access_token
        return Response({'access': str(access)}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': 'Invalid or expired refresh token', 'details': str(e)}, status=status.HTTP_401_UNAUTHORIZED)