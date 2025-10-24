from django.contrib import admin
from .models import Staff, Specialization, Doctor

# Register your models here.

admin.site.register(Staff)
admin.site.register(Specialization)
admin.site.register(Doctor)