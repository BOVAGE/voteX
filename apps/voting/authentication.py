from rest_framework import authentication, exceptions
from django.conf import settings
import jwt
from .models import Voter


class VoterJWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_data = authentication.get_authorization_header(request)
        if not auth_data:
            return None
        prefix, token = auth_data.decode("utf-8").split(" ")
        # issues when  pass_name changes  the token is no longer valid
        # hence the reason for the User.DoesNotExist exception
        try:
            payload = jwt.decode(
                token, settings.VOTER_JWT_SECRET_KEY, algorithms=["HS256"]
            )
            voter = Voter.objects.get(pass_name=payload.get("pass_name"))
            return (voter, token)
        except (jwt.DecodeError, Voter.DoesNotExist) as e:
            raise exceptions.AuthenticationFailed("Your token is invalid")
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Your Token has expired!")
