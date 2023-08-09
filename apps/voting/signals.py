import logging
from .models import Voter
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.hashers import make_password
from . import utils

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Voter)
def handle_voter_post_save(sender, instance, created, **kwargs):
    if created:
        # pass_key will be later be generated when
        # sending after verification mail to voter
        raw_password = utils.generate_password()
        print(f"{raw_password=}")
        instance.pass_key = make_password(raw_password)

        # generate pass_name
        logger.info(f"generating pass_name for {instance.email}")
        instance.pass_name = utils.generate_unique_pass_name(instance)
        instance.save()
