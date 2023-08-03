from rest_framework import serializers
from .models import Voter


class VoterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voter
        fields = "__all__"
        read_only_fields = ["election"]
