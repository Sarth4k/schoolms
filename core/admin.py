from django.contrib import admin
from .models import SchoolImage

@admin.register(SchoolImage)
class SchoolImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'image_type', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['image_type']