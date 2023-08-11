from django.urls import path
from .views import (
    VoterListCreateView,
    VoterRetrieveUpdateDeleteView,
    VoterBatchCreateView,
    VoterVerificationView,
    VoterLoginView,
    VotingView,
)

app_name = "apps.voting"
urlpatterns = [
    path(
        "<uuid:election_id>/voters",
        VoterListCreateView,
        name="list_create_ballot_question",
    ),
    path(
        "<uuid:election_id>/voters/login",
        VoterLoginView,
        name="voter_login",
    ),
    path(
        "<uuid:election_id>/votes",
        VotingView,
        name="voter_vote",
    ),
    path(
        "<uuid:election_id>/bulk-voters",
        VoterBatchCreateView,
        name="list_create_ballot_question",
    ),
    path(
        "voters/<uuid:voter_id>",
        VoterRetrieveUpdateDeleteView,
        name="retrieve_update_destroy_question",
    ),
    path(
        "voters/verify/<str:voter_id>",
        VoterVerificationView,
        name="verify_voter",
    ),
]
