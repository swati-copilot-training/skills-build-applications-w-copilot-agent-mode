from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Profile, Activity


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')
        read_only_fields = ('id', 'username', 'email')


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ('user', 'display_name', 'bio')


class ActivitySerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Activity
        fields = ('id', 'user', 'activity_type', 'date', 'duration_minutes', 'distance_km', 'calories', 'notes', 'created_at')
        read_only_fields = ('id', 'user', 'created_at')
