import logging
from .models import Voter
from django.db.models.signals import post_save
from django.dispatch import receiver
from . import utils

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Voter)
def handle_voter_post_save(sender, instance, created, **kwargs):
    if created:
        # generate pass_name
        logger.info(f"generating pass_name for {instance.email}")
        instance.pass_name = utils.generate_unique_pass_name(instance)
        instance.save()
