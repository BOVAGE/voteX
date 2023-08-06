from rest_framework import serializers
from .models import Voter


class VoterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voter
        read_only_fields = ["election"]
        exclude = ["pass_name", "pass_key"]
