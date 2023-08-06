from celery import shared_task
from apps.common.utils import send_html_email


@shared_task
def send_email_task(template_path, context, recipient):
    return send_html_email(
        template_path, context, recipient, "Votex - Complete Voter's Registration"
    )
