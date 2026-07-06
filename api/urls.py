from django.urls import path
from . import views
from rest_framework_simplejwt.views import (

TokenObtainPairView,

TokenRefreshView,
)

urlpatterns = [
    path('subjects/', views.subjects_list),
    path('token/',TokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('token/refresh/',TokenRefreshView.as_view()),
    path('subjects/<int:pk>/',views.subjects_detail),
    path('subjects/<int:pk>/delete/',views.subjects_delete),
    path('login/',views.login_view),
    path('register/',views.register_view),
    path('student/',views.student_profile),
    path('student/update/',views.student_profile_update),
    path('student/admissionstatus/',views.student_admission_status),
    path('student/enrolled/',views.student_enrolled_subjects),
]
