from rest_framework.views import APIView
from rest_framework import generics
from .serializers import (
    ElectionFullDetailSerializer,
    OptionSerializer,
    BallotQuestionSerializer,
)
from .models import Election, BallotQuestion, Option
from rest_framework.response import Response
from rest_framework import status
from apps.common.permissions import IsOwnerOrReadOnly
from django.shortcuts import get_object_or_404


class ElectionListCreateView(generics.ListCreateAPIView):
    """
    views to create and return list of elections
    created by the authenticated user
    """

    serializer_class = ElectionFullDetailSerializer

    def get_queryset(self):
        return Election.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def list(self, request, *args, **kwargs):
        data = super().list(request, *args, **kwargs).data
        data = {
            "status": "success",
            "message": "All Elections created by the authenticated user fetched successfully",
            "data": data,
        }
        return Response(data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = super().create(request, *args, **kwargs).data
        data = {
            "status": "success",
            "message": f"Election - {data.get('title')} created successfully",
            "data": data,
        }
        return Response(data, status=status.HTTP_200_OK)


class ElectionRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """
    views to retrieve, update and delete elections
    created by the authenticated user
    """

    serializer_class = ElectionFullDetailSerializer
    permission_classes = [IsOwnerOrReadOnly]
    lookup_field = "id"
    lookup_url_kwarg = "election_id"

    def get_queryset(self):
        return Election.objects.filter(created_by=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        data = super().retrieve(request, *args, **kwargs).data
        data = {
            "status": "success",
            "message": f"Election - {data.get('title')} retrieved successfully",
            "data": data,
        }
        return Response(data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        data = super().update(request, *args, **kwargs).data
        data = {
            "status": "success",
            "message": f"Election - {data.get('id')} updated successfully",
            "data": data,
        }
        return Response(data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        data = super().destroy(request, *args, **kwargs).data
        data = {
            "status": "success",
            "message": f"Election deleted successfully",
            "data": data,
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)


class BallotQuestionView(generics.ListCreateAPIView):
    """
    view to create and list ballot questions under an election
    created by the authenticated user
    """

    serializer_class = BallotQuestionSerializer

    def get_queryset(self):
        election = get_object_or_404(
            Election,
            id=self.kwargs.get("election_id"),
            created_by=self.request.user,
        )
        return election.ballot_questions.all()

    def perform_create(self, serializer):
        election = get_object_or_404(
            Election,
            id=self.kwargs.get("election_id"),
            created_by=self.request.user,
        )
        serializer.save(election=election)

    def list(self, request, *args, **kwargs):
        data = super().list(request, *args, **kwargs).data
        data = {
            "status": "success",
            "message": "All Ballot Questions for this election fetched successfully",
            "data": data,
        }
        return Response(data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = super().create(request, *args, **kwargs).data
        data = {
            "status": "success",
            "message": f"Ballot Question - {data.get('title')} created successfully",
            "data": data,
        }
        return Response(data, status=status.HTTP_200_OK)

# TODO:
# class OptionView(generics.ListCreateAPIView):
#     """
#     view to create options for a ballot question
#     """

#     serializer_class = ElectionFullDetailSerializer

#     def get_queryset(self):
#         return Election.objects.filter(created_by=self.request.user)


ElectionListCreateView = ElectionListCreateView.as_view()
ElectionRetrieveUpdateDeleteView = ElectionRetrieveUpdateDeleteView.as_view()
BallotQuestionView = BallotQuestionView.as_view()
# OptionView = OptionView.as_view()
