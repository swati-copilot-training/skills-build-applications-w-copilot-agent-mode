from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Profile, Activity, Team, Workout


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


class TeamSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all(), required=False)

    class Meta:
        model = Team
        fields = ('id', 'name', 'members', 'created_at')
        read_only_fields = ('id', 'created_at')


class ActivitySerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    team = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Activity
        fields = ('id', 'user', 'activity_type', 'date', 'duration_minutes', 'distance_km', 'calories', 'notes', 'team', 'created_at')
        read_only_fields = ('id', 'user', 'created_at')


class WorkoutSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Workout
        fields = ('id', 'user', 'title', 'date', 'duration_minutes', 'calories', 'notes', 'created_at')
        read_only_fields = ('id', 'user', 'created_at')


class LeaderboardEntrySerializer(serializers.Serializer):
    user = UserSerializer()
    total_distance_km = serializers.FloatField()
    total_duration_minutes = serializers.IntegerField()
    total_calories = serializers.IntegerField()
