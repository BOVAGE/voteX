from django.urls import path
from .views import (
    ElectionListCreateView,
    BallotQuestionView,
    BallotQuestionRetrieveUpdateDeleteView,
    OptionListCreateView,
    OptionRetrieveUpdateDeleteView,
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
    path(
        "questions/<uuid:question_id>",
        BallotQuestionRetrieveUpdateDeleteView,
        name="retrieve_update_destroy_question",
    ),
    path(
        "<uuid:election_id>/questions/<uuid:question_id>/options",
        OptionListCreateView,
        name="list_create_option",
    ),
    path(
        "options/<uuid:option_id>",
        OptionRetrieveUpdateDeleteView,
        name="retrieve_update_destroy_election",
    ),
]