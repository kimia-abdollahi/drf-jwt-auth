from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from .serializers import UserRegistrationSerializer, UserSerializer, LogoutSerializer
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserRegistrationSerializer, UserSerializer

User = get_user_model()

class RegisterView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        tags=["Auth"],
        summary="Register a new user",
        request=UserRegistrationSerializer,
        responses={
            201: UserSerializer,
            400: OpenApiResponse(description="Validation error"),
        },
        examples=[
            OpenApiExample(
                "Register example",
                value={"username": "kimia", "email": "k@example.com", "password": "Pa$$w0rd123", "first_name": "Kimia", "last_name": "A"},
                request_only=True,
            )
        ],
    )
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Me"],
        summary="Get current user's profile",
        responses={200: UserSerializer, 401: OpenApiResponse(description="Unauthorized")},
    )
    def get(self, request):
        return Response(UserSerializer(request.user).data)


class AdminOnlyView(APIView):
    permission_classes = [IsAdminUser]

    @extend_schema(
        tags=["Admin"],
        summary="Admin-only sample endpoint",
        responses={200: OpenApiResponse(description="OK"), 403: OpenApiResponse(description="Forbidden")},
    )
    def get(self, request):
        return Response({"detail": "Welcome admin! Only staff users can see this."})


class LogoutView(APIView):
    @extend_schema(
        tags=["Auth"],
        summary="Logout by blacklisting refresh token",
        request=LogoutSerializer,
        responses={205: OpenApiResponse(description="Logged out"), 400: OpenApiResponse(description="Bad Request")},
        examples=[
            OpenApiExample(
                "Logout example",
                value={"refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."},
                request_only=True,
            )
        ],
    )
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Logged out (refresh token blacklisted)."}, status=status.HTTP_205_RESET_CONTENT)
        except KeyError:
            return Response({"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({"detail": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)
