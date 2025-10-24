from django.urls import path
from . import views

app_name = 'receptionist'

urlpatterns = [
    # Patient endpoints
    path('patients/', views.PatientListCreateView.as_view(), name='patient-list-create'),
    path('patients/<int:id>/', views.PatientDetailView.as_view(), name='patient-detail'),
    
    # Appointment endpoints
    path('appointments/', views.AppointmentListCreateView.as_view(), name='appointment-list-create'),
    path('appointments/<int:id>/', views.AppointmentDetailView.as_view(), name='appointment-detail'),
    
    # Doctor endpoints (for appointment booking)
    path('doctors/', views.DoctorListView.as_view(), name='doctor-list'),
]
