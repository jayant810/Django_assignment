from django.contrib import admin
from .models import VendorProductMapping

@admin.register(VendorProductMapping)
class VendorProductMappingAdmin(admin.ModelAdmin):
    list_display = ('vendor', 'product', 'primary_mapping', 'is_active')
    list_filter = ('vendor', 'product', 'primary_mapping')
