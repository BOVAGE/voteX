from rest_framework import serializers
from .models import (
    Election,
    Option,
    BallotQuestion,
    ElectionSetting,
    ElectionSettingCategory,
    ElectionSettingParameter,
)


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = [
            "id",
            "ballot_question",
            "title",
            "short_description",
            "description",
            "image",
            "created_at",
        ]
        read_only_fields = ["ballot_question"]


class BallotQuestionSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField()

    class Meta:
        model = BallotQuestion
        fields = [
            "id",
            "election",
            "title",
            "short_description",
            "description",
            "image",
            "created_at",
            "validation_choice_max",
            "validation_choice_min",
            "options",
        ]
        read_only_fields = ["election"]

    def get_options(self, obj):
        return OptionSerializer(obj.options.all(), many=True).data


class ElectionFullDetailSerializer(serializers.ModelSerializer):
    ballot_questions = serializers.SerializerMethodField()

    class Meta:
        model = Election
        fields = [
            "id",
            "title",
            "description",
            "start_date",
            "end_date",
            "timezone",
            "created_by",
            "created_at",
            "last_updated",
            "status",
            "election_live_url",
            "election_live_short_url",
            "election_live_preview_url",
            "ballot_questions",
        ]
        read_only_fields = ["created_by"]

    def get_ballot_questions(self, obj):
        return BallotQuestionSerializer(obj.ballot_questions.all(), many=True).data


class ElectionResultSerializer(serializers.ModelSerializer):
    # ballot_questions = serializers.SerializerMethodField()

    class Meta:
        model = Election
        fields = [
            "title",
            "election_result",
            "election_result_percentage",
            "election_result_degree",
            "no_of_eligible_voters",
            "no_of_all_voters",
            "no_of_all_voters_that_have_voted",
        ]
        read_only_fields = ["created_by"]

    # def get_ballot_questions(self, obj):
    #     return BallotQuestionSerializer(obj.ballot_questions.all(), many=True).data


class ElectionSettingsSerializer(serializers.ModelSerializer):
    configurations = serializers.SerializerMethodField()

    class Meta:
        model = ElectionSetting
        fields = [
            "configurations",
        ]

    def get_configurations(self, obj):
        print(f"{obj.configurations=}")
        return ElectionSettingParameterSerializer(obj.configurations, many=True).data


class ElectionSettingParameterSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        source="category.name", read_only=True
    )
    # queryset=ElectionSettingCategory.objects.all()

    class Meta:
        model = ElectionSettingParameter
        fields = [
            "id",
            "election_setting",
            "setting_type",
            "description",
            "category",
            "title",
            "value",
        ]
        read_only_fields = [
            "election_setting",
            "setting_type",
            "description",
            "category",
            "title",
        ]
        # extra_kwargs = {
        #     "pass_key": {"write_only": True, "required": True},
        #     "pass_name": {"required": True},
        # }
