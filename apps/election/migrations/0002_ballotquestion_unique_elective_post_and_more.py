# Generated by Django 4.0 on 2023-08-03 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('election', '0001_initial'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='ballotquestion',
            constraint=models.UniqueConstraint(fields=('election', 'title'), name='unique_elective_post'),
        ),
        migrations.AddConstraint(
            model_name='option',
            constraint=models.UniqueConstraint(fields=('ballot_question', 'title'), name='unique_booking'),
        ),
    ]
