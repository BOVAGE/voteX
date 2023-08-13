from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import send_mail
import logging

logger = logging.getLogger(__name__)


def send_html_email(template_path, context, recipient, subject):
    email_body = render_to_string(template_path, context)
    logger.info(f"sending html mail to {recipient} from {settings.DEFAULT_FROM_EMAIL}")
    return send_mail(
        subject,
        email_body,
        f'{settings.DEFAULT_FROM_EMAIL}',
        [recipient],
        html_message=email_body,
    )
