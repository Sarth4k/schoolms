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
