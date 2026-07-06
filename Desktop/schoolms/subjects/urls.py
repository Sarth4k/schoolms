from django.urls import path
from .views import SubjectListView, EnrollView

urlpatterns = [
    path('', SubjectListView.as_view(), name='subject-list'),
    path('enroll/<int:subject_id>/', EnrollView.as_view(), name='enroll'),
]
