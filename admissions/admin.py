from django.contrib import admin
from django.utils import timezone
from django.utils.html import mark_safe
from .models import AdmissionRequest

@admin.register(AdmissionRequest)
class AdmissionRequestAdmin(admin.ModelAdmin):
    list_display = ['student', 'status', 'applied_at', 'document_links']
    list_filter = ['status']
    search_fields = ['student__user__first_name', 'student__user__last_name']
    actions = ['approve_admissions', 'reject_admissions']

    def document_links(self, obj):
        links = []
        if obj.birth_certificate:
            links.append(f'<a href="{obj.birth_certificate.url}" target="_blank">📄 Birth Cert</a>')
        if obj.previous_marksheet:
            links.append(f'<a href="{obj.previous_marksheet.url}" target="_blank">📄 Marksheet</a>')
        if obj.address_proof:
            links.append(f'<a href="{obj.address_proof.url}" target="_blank">📄 Address Proof</a>')
        if links:
            return mark_safe(' &nbsp;|&nbsp; '.join(links))
        return 'No documents'
    document_links.short_description = 'Documents'

    def approve_admissions(self, request, queryset):
        queryset.update(status='approved', reviewed_at=timezone.now())
    approve_admissions.short_description = "✅ Approve selected"

    def reject_admissions(self, request, queryset):
        queryset.update(status='rejected', reviewed_at=timezone.now())
    reject_admissions.short_description = "❌ Reject selected"