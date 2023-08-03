from django.contrib import admin
from .models import (
    BallotQuestion,
    Election,
    ElectionSetting,
    ElectionSettingCategory,
    ElectionSettingParameter,
    Option,
)


class OptionInlineAdmin(admin.StackedInline):
    model = Option
    list_display = ["id", "title", "short_description", "created_at"]


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "short_description", "created_at", "ballot_question"]


@admin.register(BallotQuestion)
class BallotQuestionAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "election",
        "title",
        "short_description",
        "created_at",
        "validation_choice_max",
        "validation_choice_min",
    ]
    inlines = [OptionInlineAdmin]


class BallotQuestionInlineAdmin(admin.StackedInline):
    list_display = [
        "id",
        "election",
        "title",
        "short_description",
        "created_at",
        "validation_choice_max",
        "validation_choice_min",
    ]
    model = BallotQuestion


@admin.register(Election)
class ElectionAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "description",
        "start_date",
        "end_date",
        "created_by",
        "created_at",
        "last_updated",
        "status",
    ]
    inlines = [BallotQuestionInlineAdmin]


@admin.register(ElectionSettingCategory)
class ElectionSettingCategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]


@admin.register(ElectionSetting)
class ElectionSettingAdmin(admin.ModelAdmin):
    list_display = ["id", "election"]


@admin.register(ElectionSettingParameter)
class ElectionSettingAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "election_setting",
        "setting_type",
        "title",
        "value",
        "category",
    ]
