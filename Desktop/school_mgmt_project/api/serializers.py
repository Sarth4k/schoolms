from rest_framework import serializers
from subjects.models import Subject
from accounts.models import StudentProfile


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name', 'code', 'description', 'teachers', 'students']


class StudentProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    full_name = serializers.CharField(source='user.get_full_name', read_only=True)
    admission_status = serializers.SerializerMethodField()
    enrolled_subjects = SubjectSerializer(many=True, read_only=True)

    class Meta:
        model = StudentProfile
        fields = [
            'id', 'username', 'email', 'full_name',
            'profile_photo', 'phone', 'date_of_birth',
            'address', 'guardian_name', 'guardian_phone',
            'admission_status', 'enrolled_subjects'
        ]

    def get_admission_status(self, obj):
        admission = getattr(obj, 'admissionrequest', None)
        if admission:
            return admission.status
        return None
        
