from rest_framework import serializers
from auth_app.models import UserProfile
from django.contrib.auth.models import User
from auth_app.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    # Zeigt den Namen statt nur die ID
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'username', 'bio', 'location']


class RegistrationSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(write_only=True)
    repeated_password = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password',
                  'repeated_password', 'fullname']

    def validate(self, data):
        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError("Passwords do not match.")

        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("Email is already in use.")

        return data

    def create(self, validated_data):
        fullname = validated_data.pop('fullname', '')
        name_parts = fullname.split(' ', 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ''
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=first_name,
            last_name=last_name
        )

        UserProfile.objects.create(user=user)
        return user
