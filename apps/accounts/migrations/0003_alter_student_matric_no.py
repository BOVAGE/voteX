# Generated by Django 4.0 on 2023-07-31 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_remove_guest_phone_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='matric_no',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
