from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer
from auth_app.models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class UserMiniSerializer(serializers.ModelSerializer):
    """Minimal user serializer exposing id, email and full name."""

    fullname = serializers.ReadOnlyField(source='first_name')

    class Meta:
        model = User
        fields = ['id', 'email', 'fullname']


class EmailAuthTokenSerializer(serializers.Serializer):
    """Serializer for user authentication via email."""

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """Verify credentials and return the authenticated user object."""
        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Invalid email or password.')
        data['user'] = user

        return data


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for reading and updating user profile data."""

    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'username', 'bio', 'location']


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializer for new user registration."""

    fullname = serializers.CharField(write_only=True)
    repeated_password = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'repeated_password', 'fullname']

    def validate(self, data):
        """Ensure passwords match and email is not already registered."""

        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError("Passwords do not match.")

        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("Email is already in use.")

        return data

    def create(self, validated_data):
        """Create a new User and associated UserProfile."""

        fullname = validated_data.pop('fullname', '')
        validated_data.pop('repeated_password')
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=fullname,
        )

        UserProfile.objects.create(user=user)

        return user
