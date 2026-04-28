from rest_framework import generics, status
from auth_app.models import UserProfile
from .serializers import UserProfileSerializer, EmailAuthTokenSerializer
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import RegistrationSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


class UserProfileList(generics.ListCreateAPIView):
    """List all user profiles or create a new one."""

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class UserProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a single user profile."""

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class CustomLoginView(APIView):
    """Handle user login and return an auth token."""

    permission_classes = [AllowAny]

    def post(self, request):
        """Authenticate user and return token with user info."""

        serializer = EmailAuthTokenSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, _created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.id,
                'email': user.email,
                'fullname': user.first_name,
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegistrationView(APIView):
    """Handle new user registration."""

    permission_classes = [AllowAny]

    def post(self, request):
        """Create a new user account and return token with user info."""
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _created = Token.objects.get_or_create(user=user)
            data = {
                'token': token.key,
                'user_id': user.id,
                'fullname': user.first_name,
                'email': user.email
            }
            return Response(data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
