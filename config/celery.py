import os

from celery import Celery
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.


ENVIRONMENT = os.getenv("ENV")
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "config.settings.dev"
) if ENVIRONMENT == "DEVELOPMENT" else os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "config.settings.prod"
)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
app = Celery("config")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
