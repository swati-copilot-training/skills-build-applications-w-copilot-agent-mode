from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ActivityViewSet, ProfileView

router = DefaultRouter()
router.register(r'activities', ActivityViewSet, basename='activity')

urlpatterns = [
    path('', include(router.urls)),
    path('me/profile/', ProfileView.as_view(), name='me-profile'),
]
