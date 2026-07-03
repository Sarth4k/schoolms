from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

    def is_student(self):
        return self.role == 'student'

    def is_teacher(self):
        return self.role == 'teacher'


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='studentprofile')
    profile_photo = models.ImageField(upload_to='students/', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    guardian_name = models.CharField(max_length=100, blank=True)
    guardian_phone = models.CharField(max_length=15, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - Student"

    @property
    def admission_status(self):
        try:
            return self.admissionrequest.status
        except:
            return None


class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacherprofile')
    profile_photo = models.ImageField(upload_to='teachers/', blank=True, null=True)
    bio = models.TextField(blank=True)
    phone = models.CharField(max_length=15, blank=True)
    qualification = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - Teacher"
