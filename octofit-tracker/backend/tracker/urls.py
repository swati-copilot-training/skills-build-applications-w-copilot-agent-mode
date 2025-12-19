from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ActivityViewSet, ProfileView, TeamViewSet, WorkoutViewSet, LeaderboardView

router = DefaultRouter()
router.register(r'activities', ActivityViewSet, basename='activity')
router.register(r'teams', TeamViewSet, basename='team')
router.register(r'workouts', WorkoutViewSet, basename='workout')

urlpatterns = [
    path('', include(router.urls)),
    path('me/profile/', ProfileView.as_view(), name='me-profile'),
    path('leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
]
