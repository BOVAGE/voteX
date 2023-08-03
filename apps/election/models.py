from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
import uuid

User = get_user_model()


class StatusChoices(models.TextChoices):
    BUILDING = "BUILDING", _("BUILDING")
    LIVE = "LIVE", _("LIVE")


class SettingTypeChoices(models.TextChoices):
    BOOLEAN = "BOOLEAN", _("BOOLEAN")
    TEXT = "TEXT", _("TEXT")


# Create your models here.
class Election(models.Model):
    id = models.UUIDField(
        editable=False,
        db_index=True,
        default=uuid.uuid4,
        primary_key=True,
        null=False,
        blank=False,
    )
    title = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    timezone = models.CharField(max_length=50)
    created_by = models.ForeignKey(
        User, related_name="elections", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    election_live_url = models.CharField(max_length=100, blank=True, null=True)
    election_live_short_url = models.CharField(max_length=100, blank=True, null=True)
    election_live_preview_url = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(
        choices=StatusChoices.choices, default=StatusChoices.BUILDING, max_length=50
    )

    def __str__(self):
        return self.title


class ElectionSetting(models.Model):
    id = models.UUIDField(
        editable=False,
        db_index=True,
        default=uuid.uuid4,
        primary_key=True,
        null=False,
        blank=False,
    )
    election = models.OneToOneField(Election, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.election.title} setting"


class ElectionSettingCategory(models.Model):
    id = models.UUIDField(
        editable=False,
        db_index=True,
        default=uuid.uuid4,
        primary_key=True,
        null=False,
        blank=False,
    )
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Election Setting Categories"

    def __str__(self):
        return self.name


class ElectionSettingParameter(models.Model):
    id = models.UUIDField(
        editable=False,
        db_index=True,
        default=uuid.uuid4,
        primary_key=True,
        null=False,
        blank=False,
    )
    election_setting = models.OneToOneField(ElectionSetting, on_delete=models.CASCADE)
    setting_type = models.CharField(choices=SettingTypeChoices.choices, max_length=50)
    category = models.ForeignKey(
        ElectionSettingCategory, on_delete=models.SET_NULL, null=True
    )
    title = models.CharField(max_length=50)
    value = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f"{self.title} - {self.value}"


class BallotQuestion(models.Model):
    id = models.UUIDField(
        editable=False,
        db_index=True,
        default=uuid.uuid4,
        primary_key=True,
        null=False,
        blank=False,
    )
    election = models.ForeignKey(
        Election, related_name="ballot_questions", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=100)
    short_description = models.CharField(max_length=1000)
    description = models.TextField()
    image = models.ImageField(upload_to="elections/", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    validation_choice_max = models.PositiveSmallIntegerField(default=1)
    validation_choice_min = models.PositiveSmallIntegerField(default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["election", "title"], name="unique_elective_post"
            ),
        ]

    def __str__(self):
        return self.title


class Option(models.Model):
    id = models.UUIDField(
        editable=False,
        db_index=True,
        default=uuid.uuid4,
        primary_key=True,
        null=False,
        blank=False,
    )
    ballot_question = models.ForeignKey(
        BallotQuestion, related_name="options", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=50)
    short_description = models.CharField(max_length=1000)
    description = models.TextField()
    image = models.ImageField(upload_to="elections/", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["ballot_question", "title"], name="unique_option"
            ),
        ]

    def __str__(self):
        return self.title
