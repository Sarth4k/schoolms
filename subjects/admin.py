from django.contrib import admin
from .models import Subject

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'created_at']
    filter_horizontal = ['teachers', 'students']
    search_fields = ['name', 'code']
