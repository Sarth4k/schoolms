from django.urls import path
from . import views
from rest_framework_simplejwt.views import (

TokenObtainPairView,

TokenRefreshView,
)

urlpatterns = [
    path('', views.subjects_list),
    path('token/',TokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('token/refresh/',TokenRefreshView.as_view()),
    path('<int:pk>/',views.subjects_detail),
    #path('<int:pk>/update/',views.subjects_update),
    path('<int:pk>/delete/',views.subjects_delete),
    path('login/',views.login_view),
    path('register/',views.register_view),
]
