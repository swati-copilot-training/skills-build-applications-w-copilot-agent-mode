"""WSGI config for octofit_tracker project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'octofit_tracker.settings')

try:
    application = get_wsgi_application()
except Exception as exc:
    # Provide a clearer error message during startup to help debugging
    raise RuntimeError(
        "Failed to import Django WSGI application. Verify Django is installed "
        "and DJANGO_SETTINGS_MODULE is set correctly (e.g., 'octofit_tracker.settings')."
    ) from exc
