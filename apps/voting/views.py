from rest_framework.views import APIView
from rest_framework import generics
from .serializers import VoterSerializer, VoterLoginSerializer, VoteSerializer
from .models import Voter
from apps.election.models import Election
from rest_framework.response import Response
from rest_framework import status
from .permissions import IsVoter
from apps.common.permissions import IsOwnerOrReadOnly
from django.shortcuts import get_object_or_404
from apps.common.tasks import send_email_task
from . import utils
from django.contrib.auth.hashers import make_password
import logging

from .tokens import VoterTokenGenerator
from django.urls import reverse_lazy
from django.utils.encoding import smart_bytes, smart_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework.exceptions import AuthenticationFailed, NotFound
from .authentication import VoterJWTAuthentication

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
        uidb64 = urlsafe_base64_encode(smart_bytes(data.id))
        logger.info(f"The uidb64 is {uidb64}")
        token = VoterTokenGenerator().make_token(data)
        verify_link = self.request.build_absolute_uri(
            reverse_lazy("apps.voting:verify_voter", args=(uidb64,))
        )
        verify_link += f"?token={token}"
        logger.info(f"Sending verification mail to voter with email: {data.email}")
        send_email_task.delay(
            "voting/verify_voter.html",
            {"election_title": election.title, "link": verify_link},
            data.email,
        )
        logger.info(f"The verification is {verify_link}")

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
        for voter in data:
            voter = Voter.objects.get(id=voter.get("id"))
            uidb64 = urlsafe_base64_encode(smart_bytes(voter.id))
            logger.info(f"The uidb64 is {uidb64}")
            token = VoterTokenGenerator().make_token(voter)
            verify_link = self.request.build_absolute_uri(
                reverse_lazy("apps.voting:verify_voter", args=(uidb64,))
            )
            verify_link += f"?token={token}"
            logger.info(f"Sending verification mail to voter with email: {voter.email}")
            send_email_task.delay(
                "voting/verify_voter.html",
                {"election_title": election.title, "link": verify_link},
                voter.email,
            )
            logger.info(f"The verification is {verify_link}")
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


class VoterVerificationView(generics.GenericAPIView):
    serializer_class = VoterSerializer
    permission_classes = []
    authentication_classes = []

    def get(self, request, voter_id):
        token = request.query_params.get("token")
        try:
            id = str(smart_str(urlsafe_base64_decode(voter_id)))
            voter = Voter.objects.get(id=id)
        except ValueError:
            raise AuthenticationFailed("This token is invalid")
        except Voter.DoesNotExist:
            raise NotFound("Voter does not exist")
        if not VoterTokenGenerator().check_token(voter, token):
            raise AuthenticationFailed("This token is invalid")
        voter.is_verified = True
        raw_password = utils.generate_password()
        print(f"{raw_password=}")
        voter.pass_key = make_password(raw_password)
        voter.save()
        send_email_task.delay(
            "voting/voter_cred.html",
            {
                "election_title": voter.election.title,
                "pass_name": voter.pass_name,
                "pass_key": raw_password,
            },
            voter.email,
        )
        data = {
            "status": "success",
            "message": f"voter verified and credentials has been sent to your email successfully",
            "data": None,
        }
        return Response(data, status=status.HTTP_200_OK)


class VoterLoginView(generics.GenericAPIView):
    serializer_class = VoterLoginSerializer
    permission_classes = []
    authentication_classes = []

    def post(self, request, election_id):
        serializer = self.serializer_class(
            data=request.data, context={"election_id": election_id}
        )
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        data = {
            "status": "success",
            "message": f"Voter's credentials are valid",
            "data": data,
        }
        return Response(data, status=status.HTTP_200_OK)


class VotingView(generics.GenericAPIView):
    serializer_class = VoteSerializer
    permission_classes = [IsVoter]
    authentication_classes = [VoterJWTAuthentication]

    def post(self, request, election_id):
        serializer = self.serializer_class(
            data=request.data,
            context={"election_id": election_id, "request": request},
            many=True,
        )
        serializer.is_valid(raise_exception=True)
        data = serializer.save(voter=request.user)
        data = {
            "status": "success",
            "message": f"Voting process completed successfully",
            "data": data,
        }
        return Response(data, status=status.HTTP_200_OK)


VoterListCreateView = VoterListCreateView.as_view()
VoterRetrieveUpdateDeleteView = VoterRetrieveUpdateDeleteView.as_view()
VoterBatchCreateView = VoterBatchCreateView.as_view()
VoterVerificationView = VoterVerificationView.as_view()
VoterLoginView = VoterLoginView.as_view()
VotingView = VotingView.as_view()
