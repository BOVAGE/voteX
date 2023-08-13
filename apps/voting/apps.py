from django.apps import AppConfig


class VotingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.voting"

    def ready(self) -> None:
        from . import signals
        return super().ready()