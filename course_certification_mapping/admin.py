from django.contrib import admin
from .models import CourseCertificationMapping

@admin.register(CourseCertificationMapping)
class CourseCertificationMappingAdmin(admin.ModelAdmin):
    list_display = ('course', 'certification', 'primary_mapping', 'is_active')
    list_filter = ('course', 'certification', 'primary_mapping')
