from django.db import models
from accounts.models import StudentProfile


class AdmissionRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    student = models.OneToOneField(StudentProfile, on_delete=models.CASCADE, related_name='admissionrequest')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    reason = models.TextField(blank=True, help_text='Rejection reason')
    applied_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(blank=True, null=True)

    birth_certificate = models.FileField(upload_to='admissions/birth/', blank=True, null=True)
    previous_marksheet = models.FileField(upload_to='admissions/marksheets/', blank=True, null=True)
    address_proof = models.FileField(upload_to='admissions/address/', blank=True, null=True)

    def __str__(self):
        return f"{self.student} - {self.status}"
