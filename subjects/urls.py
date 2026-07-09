from django.urls import path
from .views import SubjectListView, EnrollView, TeacherAttendanceView, StudentAttendanceView

urlpatterns = [
    path('', SubjectListView.as_view(), name='subject-list'),
    path('enroll/<int:subject_id>/', EnrollView.as_view(), name='enroll'),
    path('attendance/<int:subject_id>/', TeacherAttendanceView.as_view(), name='teacher-attendance'),
    path('my-attendance/', StudentAttendanceView.as_view(), name='student-attendance'),
]