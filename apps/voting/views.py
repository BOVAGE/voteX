from rest_framework.views import APIView
from rest_framework import generics
from .serializers import (
    VoterSerializer,
)
from .models import Voter
from apps.election.models import Election
from rest_framework.response import Response
from rest_framework import status
from apps.common.permissions import IsOwnerOrReadOnly
from django.shortcuts import get_object_or_404
from apps.common.tasks import send_email_task
import logging

logger = logging.getLogger(__name__)


class VoterListCreateView(generics.ListCreateAPIView):
    """
    views to create and return list of voters
    for an election
    """

    serializer_class = VoterSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        return Voter.objects.filter(election__id=self.kwargs.get("election_id"))

    def perform_create(self, serializer):
        election = get_object_or_404(Election, id=self.kwargs.get("election_id"))
        self.check_object_permissions(self.request, election)
        data = serializer.save(election=election)
        logger.info(f"Sending verification mail to voter with email: {data.email}")
        send_email_task.delay(
            "voting/verify_voter.html",
            {"election_title": election.title, "link": "testing.com"},
            data.email,
        )

    def list(self, request, *args, **kwargs):
        data = super().list(request, *args, **kwargs).data
        data = {
            "status": "success",
            "message": "All Voters fpr this election fetched fetched successfully",
            "data": data,
        }
        return Response(data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = super().create(request, *args, **kwargs).data
        data = {
            "status": "success",
            "message": f"Voter created successfully",
            "data": data,
        }
        return Response(data, status=status.HTTP_200_OK)


class VoterBatchCreateView(generics.GenericAPIView):
    serializer_class = VoterSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def post(self, request, election_id):
        election = get_object_or_404(Election, id=election_id)
        self.check_object_permissions(request, election)
        serializer = self.serializer_class(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(election=election)
        data = serializer.data
        data = {
            "status": "success",
            "message": f"{len(data)} voters created successfully",
            "data": data,
        }
        return Response(data, status=status.HTTP_201_CREATED)


class VoterRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """
    views to retrieve, update and delete voters
    for an election
    """

    serializer_class = VoterSerializer
    permission_classes = [IsOwnerOrReadOnly]
    lookup_field = "id"
    lookup_url_kwarg = "voter_id"

    def get_queryset(self):
        return Voter.objects.all()

    def retrieve(self, request, *args, **kwargs):
        data = super().retrieve(request, *args, **kwargs).data
        data = {
            "status": "success",
            "message": f"Voter - {data.get('id')} retrieved successfully",
            "data": data,
        }
        return Response(data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        data = super().update(request, *args, **kwargs).data
        data = {
            "status": "success",
            "message": f"Voter - {data.get('id')} updated successfully",
            "data": data,
        }
        return Response(data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        data = super().destroy(request, *args, **kwargs).data
        data = {
            "status": "success",
            "message": f"Voter deleted successfully",
            "data": data,
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)


VoterListCreateView = VoterListCreateView.as_view()
VoterRetrieveUpdateDeleteView = VoterRetrieveUpdateDeleteView.as_view()
VoterBatchCreateView = VoterBatchCreateView.as_view()
