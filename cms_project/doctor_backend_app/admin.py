from django.contrib import admin
from .models import Consultation, MedicinePrescription, LabPrescription


@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ['id', 'consultationId', 'AppointmentId', 'Created_At']
    list_filter = ['Created_At']
    search_fields = ['consultationId', 'AppointmentId__AppointmentId']
    readonly_fields = ['consultationId', 'Created_At', 'Updated_At']


@admin.register(MedicinePrescription)
class MedicinePrescriptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'medPrescriptionId', 'consultation', 'Created_At']
    list_filter = ['Created_At']
    search_fields = ['medPrescriptionId', 'consultation__consultationId']
    readonly_fields = ['medPrescriptionId', 'Created_At', 'Updated_At']


@admin.register(LabPrescription)
class LabPrescriptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'labPrescriptionId', 'consultation', 'Created_At']
    list_filter = ['Created_At']
    search_fields = ['labPrescriptionId', 'consultation__consultationId']
    readonly_fields = ['labPrescriptionId', 'Created_At', 'Updated_At']
