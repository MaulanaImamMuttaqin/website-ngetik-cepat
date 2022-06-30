from django.urls import path

from .views import Login, MyTokenObtainPairView, RegisterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('token/obtain/', MyTokenObtainPairView.as_view(), name='token_get'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', Login.as_view()),
    path('register/', RegisterView.as_view(), name="auth_register")
]