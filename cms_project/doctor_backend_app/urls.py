from django.urls import path
from . import views

urlpatterns = [
    # Consultation endpoints
    path('consultations/', views.ConsultationListCreateView.as_view(), name='consultation-list-create'),
    path('consultations/start/', views.start_consultation, name='start-consultation'),
    path('consultations/<int:consultation_id>/status/', views.update_consultation_status, name='update-consultation-status'),
    path('consultations/<int:consultation_id>/notes/', views.update_consultation_notes, name='update-consultation-notes'),
    
    # Medicine Prescription endpoints
    path('medicine-prescriptions/', views.MedicinePrescriptionListCreateView.as_view(), name='medicine-prescription-list-create'),
    
    # Lab Prescription endpoints
    path('lab-prescriptions/', views.LabPrescriptionListCreateView.as_view(), name='lab-prescription-list-create'),
    
]

