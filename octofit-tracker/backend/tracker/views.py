from django.db.models import Sum
from rest_framework import viewsets, generics, permissions, views, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from .models import Profile, Activity, Team, Workout
from .serializers import (
    ProfileSerializer,
    ActivitySerializer,
    TeamSerializer,
    WorkoutSerializer,
    LeaderboardEntrySerializer,
)

User = get_user_model()


class ActivityViewSet(viewsets.ModelViewSet):
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Activity.objects.filter(user=self.request.user).order_by('-date')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class WorkoutViewSet(viewsets.ModelViewSet):
    serializer_class = WorkoutSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Workout.objects.filter(user=self.request.user).order_by('-date')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TeamViewSet(viewsets.ModelViewSet):
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Users see teams they belong to
        return Team.objects.filter(members=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        team = serializer.save()
        team.members.add(self.request.user)


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        return profile


class LeaderboardView(views.APIView):
    """Return top users by aggregated activity metrics (distance, duration, calories)."""
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        # Optional query params: ?limit=10&days=30
        limit = int(request.query_params.get('limit', 10))
        days = request.query_params.get('days')

        queryset = Activity.objects.all()
        if days:
            from django.utils import timezone
            from datetime import timedelta

            since = timezone.now() - timedelta(days=int(days))
            queryset = queryset.filter(date__gte=since)

        agg = (
            queryset
            .values('user')
            .annotate(
                total_distance_km=Sum('distance_km'),
                total_duration_minutes=Sum('duration_minutes'),
                total_calories=Sum('calories'),
            )
            .order_by('-total_distance_km')[:limit]
        )

        # Fetch user objects and serialize entries
        user_map = {u.id: u for u in User.objects.filter(id__in=[a['user'] for a in agg])}
        entries = []
        for a in agg:
            user_obj = user_map.get(a['user'])
            entries.append(
                {
                    'user': UserSerializer(user_obj).data,
                    'total_distance_km': a['total_distance_km'] or 0.0,
                    'total_duration_minutes': int(a['total_duration_minutes'] or 0),
                    'total_calories': int(a['total_calories'] or 0),
                }
            )

        serializer = LeaderboardEntrySerializer(entries, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)