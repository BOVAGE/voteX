import logging
from .models import (
    Election,
    ElectionSetting,
    ElectionSettingParameter,
    ElectionSettingCategory,
)
from django.db.models.signals import post_save
from django.dispatch import receiver
from . import utils
import os
import json

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Election)
def handle_election_post_save(sender, instance, created, **kwargs):
    file_path = (
        f"{os.path.dirname(os.path.abspath(__file__))}\data\default_setting.json"
    )
    print(file_path)
    if created:
        # create election setting for election
        logger.info(f"Creating Election setting for {instance.title}")
        election_setting = ElectionSetting.objects.get_or_create(election=instance)

        # create default election setting configuration

        default_settings = utils.get_json_data(file_path)
        logger.info(f"Creating default election setting configuration {instance.title}")
        parameters = default_settings.values()
        for parameters_list in parameters:
            create_setting_parameters(parameters_list, election_setting[0])
        logger.info(
            f"Done creating default election setting configuration for {instance.title}"
        )


def create_setting_parameters(parameters, election_setting):
    for parameter_detail in parameters:
        category_name = parameter_detail.pop("category")
        # title = parameter_detail.get("title")
        # value = parameter_detail.get("value")
        # type = parameter_detail.get("type")
        # description = parameter_detail.get("description")
        category = ElectionSettingCategory.objects.get(name=category_name)
        ElectionSettingParameter.objects.create(
            election_setting=election_setting, category=category, **parameter_detail
        )
