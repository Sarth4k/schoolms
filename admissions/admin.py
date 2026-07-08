from django.contrib import admin
from django.utils import timezone
from django.utils.html import mark_safe
from django.core.mail import send_mail
from django.conf import settings
from .models import AdmissionRequest


#admission status email on rejection and approve
@admin.register(AdmissionRequest)
class AdmissionRequestAdmin(admin.ModelAdmin):
    list_display = ['student', 'status', 'applied_at', 'document_links']
    list_filter = ['status']
    search_fields = ['student__user__first_name', 'student__user__last_name']
    actions = ['approve_admissions', 'reject_admissions']
    readonly_fields = ['view_birth_certificate', 'view_marksheet', 'view_address_proof', 'applied_at']

    fieldsets = (
        ('Student Info', {
            'fields': ('student', 'status', 'reason')
        }),
        ('Documents', {
            'fields': ('view_birth_certificate', 'view_marksheet', 'view_address_proof')
        }),
        ('Timestamps', {
            'fields': ('applied_at', 'reviewed_at')
        }),
    )

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

    def view_birth_certificate(self, obj):
        if obj.birth_certificate:
            return mark_safe(f'<a href="{obj.birth_certificate.url}" target="_blank">View Birth Certificate</a>')
        return 'Not uploaded'
    view_birth_certificate.short_description = 'Birth Certificate'

    def view_marksheet(self, obj):
        if obj.previous_marksheet:
            return mark_safe(f'<a href="{obj.previous_marksheet.url}" target="_blank">View Marksheet</a>')
        return 'Not uploaded'
    view_marksheet.short_description = 'Previous Marksheet'

    def view_address_proof(self, obj):
        if obj.address_proof:
            return mark_safe(f'<a href="{obj.address_proof.url}" target="_blank">View Address Proof</a>')
        return 'Not uploaded'
    view_address_proof.short_description = 'Address Proof'

    def approve_admissions(self, request, queryset):
        for admission in queryset:
            admission.status = 'approved'
            admission.reviewed_at = timezone.now()
            admission.save()

            # Email bhejo
            student_email = admission.student.user.email
            student_name = admission.student.user.get_full_name()
            if student_email:
                send_mail(
                    subject='🎉 Admission Approved - SchoolMS',
                    message=f'''Dear {student_name},

Congratulations! Your admission application has been approved.

You can now login and enroll in subjects.

Login here: http://35.154.5.116:8080/accounts/login/

Best regards,
SchoolMS Team''',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[student_email],
                    fail_silently=True,
                )
        self.message_user(request, f'{queryset.count()} admission(s) approved and emails sent!')
    approve_admissions.short_description = "✅ Approve selected"

    def reject_admissions(self, request, queryset):
        for admission in queryset:
            admission.status = 'rejected'
            admission.reviewed_at = timezone.now()
            admission.save()

            # Email bhejo
            student_email = admission.student.user.email
            student_name = admission.student.user.get_full_name()
            if student_email:
                send_mail(
                    subject='❌ Admission Status - SchoolMS',
                    message=f'''Dear {student_name},

We regret to inform you that your admission application has been rejected.

Reason: {admission.reason if admission.reason else 'Not specified'}

If you have any questions, please contact us.

Best regards,
SchoolMS Team''',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[student_email],
                    fail_silently=True,
                )
        self.message_user(request, f'{queryset.count()} admission(s) rejected and emails sent!')
    reject_admissions.short_description = "❌ Reject selected"