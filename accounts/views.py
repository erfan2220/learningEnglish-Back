from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status


# Protected view example (for authenticated users)
class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "You are authenticated!"})

# Custom Token Obtain Pair View (handles login and generates tokens)
class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return response

# Register View (Handles user registration)
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

# Login View (You can use CustomTokenObtainPairView as the login view)
class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


# Token Refresh View (for refreshing access tokens)
class TokenRefreshView(TokenRefreshView):
    pass

