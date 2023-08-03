from django.db import models
from django.db.models import Q
from apps.election.models import Election
from phonenumber_field.modelfields import PhoneNumberField
import uuid
from . import utils


class Voter(models.Model):
    id = models.UUIDField(
        editable=False,
        db_index=True,
        default=uuid.uuid4,
        primary_key=True,
        null=False,
        blank=False,
    )
    email = models.EmailField()
    phone_number = PhoneNumberField()
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    pass_name = models.CharField(max_length=100, blank=True)
    pass_key = models.CharField(max_length=100, blank=True)
    is_verified = models.BooleanField(default=False)

    class Meta:
        # email or phone_number should be unique together with election
        constraints = [
            models.UniqueConstraint(
                fields=["election", "email"],
                name="unique_voter_email",
            ),
            models.UniqueConstraint(
                fields=["election", "phone_number"],
                name="unique_voter_phone_number",
            ),
        ]

    def save(self, *args, **kwargs):
        # generate pass_name & pass_key
        self.pass_key = utils.generate_password()
        self.pass_name = utils.generate_unique_pass_name(self)
        super().save(*args, **kwargs)
