from django.urls import path
from .views import (
    ElectionListCreateView,
    BallotQuestionView,
    # OptionView,
    ElectionRetrieveUpdateDeleteView,
)

urlpatterns = [
    path("", ElectionListCreateView, name="list_create_election"),
    path(
        "<uuid:election_id>",
        ElectionRetrieveUpdateDeleteView,
        name="retrieve_update_destroy_election",
    ),
    path(
        "<uuid:election_id>/questions",
        BallotQuestionView,
        name="list_create_ballot_question",
    ),
    # path(
    #     "<uuid:election_id>/Questions/<uuid:question_id>/Options",
    #     OptionView,
    #     name="list_create_option",
    # ),
]
