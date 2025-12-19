from django.http import JsonResponse


def health(request):
    """Simple health check endpoint."""
    return JsonResponse({"status": "ok"})


def root(request):
    """Root endpoint, same as health check for now."""
    return health(request)
