from django.urls import path
from .views import RegisterView, CustomTokenObtainPairView, ProtectedView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('protected/', ProtectedView.as_view(), name='protected'),  # Example protected view
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Token refresh endpoint
]
