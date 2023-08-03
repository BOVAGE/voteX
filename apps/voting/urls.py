from django.urls import path
from .views import (
    VoterListCreateView,
    VoterRetrieveUpdateDeleteView,
    VoterBatchCreateView,
)

urlpatterns = [
    path(
        "<uuid:election_id>/voters",
        VoterListCreateView,
        name="list_create_ballot_question",
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
]
