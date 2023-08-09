from rest_framework import serializers
from .models import Voter
from django.contrib.auth.hashers import check_password
import jwt
from django.conf import settings


class VoterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voter
        read_only_fields = ["election"]
        exclude = ["pass_name", "pass_key"]


class VoterLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voter
        exclude = ["election", "phone_number", "email"]
        extra_kwargs = {
            "pass_key": {"write_only": True, "required": True},
            "pass_name": {"required": True},
        }

    def validate(self, attrs):
        voter = self.Meta.model.objects.filter(pass_name=attrs.get("pass_name")).first()
        if voter is None:
            raise serializers.ValidationError("Voter does not exist.")
        if not check_password(attrs.get("pass_key"), voter.pass_key):
            raise serializers.ValidationError("Invalid credentials")
        if not voter.is_verified:
            raise serializers.ValidationError("Voter's email is not verified")
        return super().validate(attrs)

    def save(self):
        pass_name = self.validated_data["pass_name"]
        token = jwt.encode(
            {"pass_name": pass_name}, settings.VOTER_JWT_SECRET_KEY, algorithm="HS256"
        )
        return {"access_token": token}
