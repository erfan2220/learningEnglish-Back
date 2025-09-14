# accounts/urls.py

from django.urls import path
from .views import (
    RegisterView,
    CustomTokenObtainPairView,
    ProtectedView,
    CookieTokenRefreshView,
    MeView,
    LogoutView,
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomTokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", CookieTokenRefreshView.as_view(), name="token_refresh"),
    path("protected/", ProtectedView.as_view(), name="protected"),
    path("me/", MeView.as_view(), name="me"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
