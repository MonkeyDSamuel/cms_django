from django.contrib import admin
from .models import Patient, Appointment

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['PatientId', 'Name', 'Age', 'Gender', 'PhoneNumber', 'IsActive', 'Created_At']
    list_filter = ['Gender', 'IsActive', 'Created_At']
    search_fields = ['PatientId', 'Name', 'PhoneNumber']
    readonly_fields = ['PatientId', 'Created_At', 'Updated_At']
    ordering = ['PatientId']
    
    fieldsets = (
        ('Patient Information', {
            'fields': ('PatientId', 'Name', 'Age', 'Height', 'Weight', 'Gender', 'DOB')
        }),
        ('Contact Information', {
            'fields': ('PhoneNumber', 'EmergencyNumber', 'Address')
        }),
        ('Status', {
            'fields': ('IsActive',)
        }),
        ('Timestamps', {
            'fields': ('Created_At', 'Updated_At'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['AppointmentId', 'DoctorId', 'TokenNo', 'Date', 'Status', 'Created_At']
    list_filter = ['Status', 'Date', 'DoctorId', 'Created_At']
    search_fields = ['AppointmentId', 'DoctorId__StaffId__FirstName', 'DoctorId__StaffId__LastName']
    readonly_fields = ['AppointmentId', 'Created_At']
    ordering = ['Date', 'TokenNo']
    
    fieldsets = (
        ('Appointment Information', {
            'fields': ('AppointmentId', 'DoctorId', 'TokenNo', 'Date', 'Status')
        }),
        ('Timestamps', {
            'fields': ('Created_At',),
            'classes': ('collapse',)
        }),
    )
