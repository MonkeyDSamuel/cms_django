from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    path('signup/', views.signup_user, name='signup'),
    path('signup/minimal/', views.minimal_signup, name='minimal_signup'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/', views.user_profile, name='profile'),
    path('check-role/', views.check_user_role, name='check_role'),
    path('refresh/', views.refresh_token, name='refresh_token'),
] 