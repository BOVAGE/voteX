from rest_framework import serializers
from .models import Voter
from django.contrib.auth.hashers import check_password
import jwt
from django.conf import settings
from apps.election.models import Election, BallotQuestion, Option
from django.utils import timezone
from rest_framework.exceptions import NotFound


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


class OptionSerializer(serializers.Serializer):
    option_id = serializers.CharField(write_only=True)


class VoteSerializer(serializers.Serializer):
    ballot_question_id = serializers.CharField(write_only=True)
    choices = OptionSerializer(many=True)

    def validate_choices(self, value):
        """ensure that the Option object that corresponds
        to the option_id(s) in choices exist in the database"""
        is_all_choices_valid = all(
            [
                Option.objects.filter(id=choice.get("option_id")).exists()
                for choice in value
            ]
        )
        if not is_all_choices_valid:
            raise serializers.ValidationError(
                "Invalid choice. One or more of the choice does not exist"
            )
        return value

    def validate(self, attrs):
        # print(self.context)
        # print(attrs.get("choices"))
        attrs = super().validate(attrs)
        election = Election.objects.filter(id=self.context.get("election_id")).first()
        ballot_question = BallotQuestion.objects.filter(
            id=attrs.get("ballot_question_id"), election=election
        ).first()
        if ballot_question is None:
            raise NotFound("Ballot Question does not exist.", 404)
        if election is None:
            raise NotFound("Election does not exist.", 404)
        if not (election.start_date <= timezone.now() < election.end_date):
            raise serializers.ValidationError(
                "The election has come to an end or has not started"
            )
        if election.status != "LIVE":
            raise serializers.ValidationError("The election is not LIVE yet")
        if (
            len(attrs.get("choices")) > ballot_question.validation_choice_max
            or len(attrs.get("choices")) < ballot_question.validation_choice_min
        ):
            raise serializers.ValidationError(
                f"You cannot vote for more than {ballot_question.validation_choice_max} or less than {ballot_question.validation_choice_min}"
            )
        voter = self.context.get("request").user
        can_vote = Option.can_vote(voter, ballot_question)
        if not can_vote:
            raise serializers.ValidationError(
                f"Already voted"
            )
        return attrs

    def create(self, validated_data):
        voter = validated_data.pop("voter")
        choices = validated_data.get("choices")
        for choice in choices:
            option_id = choice.get("option_id")
            # since it been validated that Option object exist in the validation
            option = Option.objects.get(id=option_id)
            option.voters.add(voter)
            option.save()
        return {"choices": choices, **validated_data}
