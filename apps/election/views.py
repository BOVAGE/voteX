from rest_framework.views import APIView
from rest_framework import generics
from .serializers import (
    ElectionFullDetailSerializer,
    OptionSerializer,
    BallotQuestionSerializer,
    ElectionResultSerializer,
    ElectionSettingsSerializer,
    ElectionSettingParameterSerializer,
    ElectionLaunchSerializer,
    ElectionAllDetailsSerializer,
)
from .models import (
    Election,
    BallotQuestion,
    Option,
    ElectionSetting,
    ElectionSettingParameter,
)
from rest_framework.response import Response
from rest_framework import status
from apps.common.permissions import IsOwnerOrReadOnly, IsOwner
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.exceptions import NotFound


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

    permission_classes = [IsOwnerOrReadOnly]
    lookup_field = "id"
    lookup_url_kwarg = "election_id"

    def get_queryset(self):
        return Election.objects.all()

    def get_serializer_class(self):
        print(f"{self.request.query_params.get('type')=}")
        if self.request.query_params.get("type") == "full":
            return ElectionAllDetailsSerializer
        return ElectionFullDetailSerializer

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
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        election = get_object_or_404(Election, id=self.kwargs.get("election_id"))
        self.check_object_permissions(self.request, election)
        return BallotQuestion.objects.all()

    def perform_create(self, serializer):
        election = get_object_or_404(Election, id=self.kwargs.get("election_id"))
        self.check_object_permissions(self.request, election)
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


class BallotQuestionRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """
    views to retrieve, update and delete ballot question
    created by the authenticated user
    """

    serializer_class = BallotQuestionSerializer
    permission_classes = [IsOwnerOrReadOnly]
    lookup_field = "id"
    lookup_url_kwarg = "question_id"

    def get_queryset(self):
        return BallotQuestion.objects.all()

    def retrieve(self, request, *args, **kwargs):
        data = super().retrieve(request, *args, **kwargs).data
        data = {
            "status": "success",
            "message": f"Ballot question - {data.get('title')} retrieved successfully",
            "data": data,
        }
        return Response(data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        data = super().update(request, *args, **kwargs).data
        data = {
            "status": "success",
            "message": f"Ballot question - {data.get('id')} updated successfully",
            "data": data,
        }
        return Response(data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        data = super().destroy(request, *args, **kwargs).data
        data = {
            "status": "success",
            "message": f"Ballot question deleted successfully",
            "data": data,
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)


class OptionListCreateView(generics.ListCreateAPIView):
    """
    view to create options for a ballot question
    """

    serializer_class = OptionSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        election = get_object_or_404(Election, id=self.kwargs.get("election_id"))
        self.check_object_permissions(self.request, election)
        return Option.objects.all()

    def perform_create(self, serializer):
        election = get_object_or_404(Election, id=self.kwargs.get("election_id"))
        ballot_question = get_object_or_404(
            election.ballot_questions, id=self.kwargs.get("question_id")
        )
        self.check_object_permissions(self.request, ballot_question)
        serializer.save(ballot_question=ballot_question)

    def list(self, request, *args, **kwargs):
        data = super().list(request, *args, **kwargs).data
        data = {
            "status": "success",
            "message": "All Options for this ballot question fetched successfully",
            "data": data,
        }
        return Response(data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = super().create(request, *args, **kwargs).data
        data = {
            "status": "success",
            "message": f"Option - {data.get('title')} created successfully",
            "data": data,
        }
        return Response(data, status=status.HTTP_200_OK)


class OptionRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """
    views to retrieve, update and delete option
    created by the authenticated user
    """

    serializer_class = OptionSerializer
    permission_classes = [IsOwnerOrReadOnly]
    lookup_field = "id"
    lookup_url_kwarg = "option_id"

    def get_queryset(self):
        return Option.objects.all()

    def retrieve(self, request, *args, **kwargs):
        data = super().retrieve(request, *args, **kwargs).data
        data = {
            "status": "success",
            "message": f"Option - {data.get('title')} retrieved successfully",
            "data": data,
        }
        return Response(data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        data = super().update(request, *args, **kwargs).data
        data = {
            "status": "success",
            "message": f"Option - {data.get('id')} updated successfully",
            "data": data,
        }
        return Response(data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        data = super().destroy(request, *args, **kwargs).data
        data = {
            "status": "success",
            "message": f"Option deleted successfully",
            "data": data,
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)


class ElectionResultView(generics.RetrieveAPIView):
    serializer_class = ElectionResultSerializer
    permission_classes = [IsOwnerOrReadOnly]
    lookup_field = "id"
    lookup_url_kwarg = "election_id"
    queryset = Election.objects.all()

    def retrieve(self, request, *args, **kwargs):
        data = super().retrieve(request, *args, **kwargs).data
        data = {
            "status": "success",
            "message": f"Election result for - {data.get('title')} retrieved successfully",
            "data": data,
        }
        return Response(data, status=status.HTTP_200_OK)


class ElectionSettingView(generics.GenericAPIView):
    serializer_class = ElectionSettingParameterSerializer
    permission_classes = [IsOwner]

    def get(self, request, election_id):
        category = request.query_params.get("category", None)

        election_setting = get_object_or_404(ElectionSetting, election__id=election_id)
        election = election_setting.election
        print(election)
        self.check_object_permissions(request, election)
        if category is not None:
            serializer = self.serializer_class(
                instance=election_setting.get_configurations_by(category), many=True
            )
        else:
            serializer = self.serializer_class(
                instance=election_setting.configurations, many=True
            )
        data = {
            "status": "success",
            "message": f"Election setting for {election.title} retrieved successfully",
            "data": serializer.data,
        }
        return Response(data, status=status.HTTP_200_OK)

    def patch(self, request, election_id):
        election_setting = get_object_or_404(ElectionSetting, election__id=election_id)
        election = election_setting.election
        print(election)
        self.check_object_permissions(request, election)
        instance = ElectionSettingParameter.objects.get(id=request.data.pop("id"))
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            "status": "success",
            "message": "Election setting Updated Successfully",
            "data": serializer.data,
        }
        return Response(data, status.HTTP_200_OK)


class ElectionLaunchView(generics.GenericAPIView):
    serializer_class = ElectionLaunchSerializer
    permission_classes = [IsOwner]

    def get(self, request, election_id):
        election = get_object_or_404(Election, id=self.kwargs.get("election_id"))
        self.check_object_permissions(self.request, election)
        serializer = self.serializer_class(instance=election)
        serializer.save()
        data = serializer.data
        data = {
            "status": "success",
            "message": f"Election {election.title} launched successfully",
            "data": serializer.data,
        }
        return Response(data, status=status.HTTP_200_OK)


class ElectionByCodeView(generics.GenericAPIView):
    serializer_class = ElectionFullDetailSerializer
    permission_classes = []

    def get(self, request, election_code):
        election = Election.objects.filter(
            Q(live_code=election_code) | Q(preview_code=election_code)
        ).first()
        if election is None:
            raise NotFound("Election with this code does not exist")
        serializer = self.serializer_class(election)
        data = serializer.data
        election_mode = election.get_mode(election_code)
        data.setdefault("mode", election_mode)
        data = {
            "status": "success",
            "message": f"Election {election.title} retrieved successfully",
            "data": data,
        }
        return Response(data, status=status.HTTP_200_OK)


ElectionListCreateView = ElectionListCreateView.as_view()
ElectionRetrieveUpdateDeleteView = ElectionRetrieveUpdateDeleteView.as_view()
BallotQuestionView = BallotQuestionView.as_view()
BallotQuestionRetrieveUpdateDeleteView = (
    BallotQuestionRetrieveUpdateDeleteView.as_view()
)
OptionListCreateView = OptionListCreateView.as_view()
OptionRetrieveUpdateDeleteView = OptionRetrieveUpdateDeleteView.as_view()
ElectionResultView = ElectionResultView.as_view()
ElectionSettingView = ElectionSettingView.as_view()
ElectionLaunchView = ElectionLaunchView.as_view()
ElectionByCodeView = ElectionByCodeView.as_view()
