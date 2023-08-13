import os
from pathlib import Path

from django.core.management.base import BaseCommand
from apps.election.models import ElectionSettingCategory
from apps.election.utils import get_json_data


APP_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = APP_DIR / "data"
FILE_PATH = DATA_DIR / "default_setting.json"


class Command(BaseCommand):
    help = "Load default election setting category to the database"

    def handle(self, *args, **options):
        data = get_json_data(file_path=FILE_PATH).keys()
        categories_list = []
        for category_name in data:
            categories_list.append(ElectionSettingCategory(name=category_name))
        ElectionSettingCategory.objects.bulk_create(categories_list)
        self.stdout.write(
            self.style.SUCCESS(
                "All Default Election category has been created Successfully"
            )
        )
