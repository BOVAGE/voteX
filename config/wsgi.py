"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

ENVIRONMENT = os.getenv("ENV")
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "config.settings.dev"
) if ENVIRONMENT == "DEVELOPMENT" else os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "config.settings.prod"
)

application = get_wsgi_application()
