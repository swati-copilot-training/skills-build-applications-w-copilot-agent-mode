from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response


def health(request):
    """Simple health check endpoint."""
    return JsonResponse({"status": "ok"})


@api_view(['GET'])
def api_root(request, format=None):
    """API root providing links to main endpoints."""
    return Response({
        'activities': reverse('tracker:activity-list', request=request, format=format),
        'teams': reverse('tracker:team-list', request=request, format=format),
        'workouts': reverse('tracker:workout-list', request=request, format=format),
        'profile': request.build_absolute_uri('/api/me/profile/'),
        'auth': request.build_absolute_uri('/api/auth/'),
        'health': request.build_absolute_uri('/health/'),
    })
