# accounts/views.py
from typing import Optional
from django.http import QueryDict
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_spectacular.utils import extend_schema
from .serializers import ForgotPasswordSerializer,ResetPasswordSerializer
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView as _TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, MeSerializer

ACCESS_MAX_AGE = 15 * 60
REFRESH_MAX_AGE = 7 * 24 * 3600

def set_auth_cookies(resp: Response, access: str, refresh: Optional[str]):
    resp.set_cookie(
        "access_token", access,
        max_age=ACCESS_MAX_AGE,
        httponly=True,
        samesite="Lax",
        secure=False,
        path="/",
    )
    if refresh:
        resp.set_cookie(
            "refresh_token", refresh,
            max_age=REFRESH_MAX_AGE,
            httponly=True,
            samesite="Lax",
            secure=False,
            path="/",
        )

def clear_auth_cookies(resp: Response):
    resp.delete_cookie("access_token", path="/")
    resp.delete_cookie("refresh_token", path="/")

class ProtectedView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        return Response({"message": "You are authenticated!"})

class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    # Default serializer uses USERNAME_FIELD (email) — works with your custom user

    def post(self, request, *args, **kwargs):
        res = super().post(request, *args, **kwargs)
        access = res.data.get("access")
        refresh = res.data.get("refresh")

        out = Response({"ok": True, "access": access, "refresh": refresh}, status=status.HTTP_200_OK)
        set_auth_cookies(out, access, refresh)
        return out

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    # Immediately log in after successful register
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)

        out = Response(MeSerializer(user).data, status=status.HTTP_201_CREATED)
        set_auth_cookies(out, access, str(refresh))
        return out

class CookieTokenRefreshView(_TokenRefreshView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        # accept refresh from cookie if not provided in body
        if not request.data.get("refresh"):
            cookie_refresh = request.COOKIES.get("refresh_token")
            if cookie_refresh:
                if isinstance(request.data, QueryDict):
                    request.data._mutable = True
                request.data["refresh"] = cookie_refresh

        res = super().post(request, *args, **kwargs)
        # When refresh succeeds, rotate access cookie
        access = res.data.get("access")
        if res.status_code == 200 and access:
            out = Response({"ok": True}, status=status.HTTP_200_OK)
            set_auth_cookies(out, access, None)
            return out
        return res


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(MeSerializer(request.user).data, status=status.HTTP_200_OK)

class LogoutView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        refresh = request.COOKIES.get("refresh_token")
        if refresh:
            try:
                token = RefreshToken(refresh)
                token.blacklist()  # works only if blacklist app enabled
            except Exception:
                pass
        resp = Response({"ok": True}, status=status.HTTP_200_OK)
        clear_auth_cookies(resp)
        return resp


# accounts/views.py

class ForgotPasswordView(APIView):
    """
    Step 1: User requests a password reset by providing their email address.
    """
    permission_classes = [AllowAny]

    @extend_schema(
        request=ForgotPasswordSerializer,
        responses={200: "Password reset link has been sent."}
    )

    def post(self, request):
        email = request.data.get('email')

        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = get_user_model().objects.get(email=email)
        except get_user_model().DoesNotExist:
            return Response({"error": "User with this email does not exist"}, status=status.HTTP_404_NOT_FOUND)

        # If the email is valid, ask for the new password directly
        return Response({"message": "Email exists. Please provide a new password."}, status=status.HTTP_200_OK)


class ResetPasswordView(APIView):
    """
    Step 2: User submits their new password to reset it.
    """
    permission_classes = [AllowAny]

    @extend_schema(
        request=ResetPasswordSerializer,
        responses={200: "Password reset link has been sent."}
    )

    def post(self, request):
        email = request.data.get('email')
        new_password = request.data.get('new_password')

        if not email or not new_password:
            return Response({"error": "Email and new password are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Find the user by email
        try:
            user = get_user_model().objects.get(email=email)
        except get_user_model().DoesNotExist:
            return Response({"error": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)

        # Set the new password
        user.set_password(new_password)
        user.save()

        return Response({"message": "Password has been successfully updated."}, status=status.HTTP_200_OK)
