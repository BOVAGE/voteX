from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .models import Voter


class VoterTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, voter: Voter, timestamp: int) -> str:
        email = voter.email
        is_verified = voter.is_verified
        return f"{voter.id}{voter.pass_name}{is_verified}{timestamp}{email}"
