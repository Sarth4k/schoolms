from django.db import models
from accounts.models import TeacherProfile, StudentProfile


class Subject(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    teachers = models.ManyToManyField(TeacherProfile, related_name='subjects', blank=True)
    students = models.ManyToManyField(StudentProfile, related_name='enrolled_subjects', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code} - {self.name}"


class Attendance(models.Model):
    STATUS_CHOICES = (
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
    )
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='attendances')
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='absent')
    marked_by = models.ForeignKey(TeacherProfile, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['subject', 'student', 'date']

    def __str__(self):
        return f"{self.student} - {self.subject} - {self.date} - {self.status}"
