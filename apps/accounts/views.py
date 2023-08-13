from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserSerializer, TokenObtainPairSerializer
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib import messages
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser

"""class RegisterView(APIView):
    http_method_names = ['post']

    def post(self, *args, **kwargs):
        serializer = UserSerializer(data=self.request.data)
        if serializer.is_valid():
            user_type = serializer.validated_data.get('user_type')
            extra_fields = {}

            if user_type == 'student':
                extra_fields['matric_no'] = serializer.validated_data.pop('matric_no', None)

            user = get_user_model().objects.create_user(**serializer.validated_data, **extra_fields)

            message = 'User created successfully.'
            return Response(status=HTTP_201_CREATED, data={'message': message, 'user_id': user.id})
        return Response(status=HTTP_400_BAD_REQUEST, data={'errors': serializer.errors})"""


class RegisterView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # import logging
        data = request.data
        # logger = logging.getLogger('accounts')
        # logger.info('inside post')
        # logger.info(data)
        serializer = self.get_serializer(data=data, context={"request": request})
        if serializer.is_valid():
            # logger.info('serializer is valid')
            user = serializer.save()
            data = serializer.data

            print(user)
            return Response(
                {"message": "User Created successful", "data": serializer.data},
                status=200,
            )
        error_keys = list(serializer.errors.keys())
        if error_keys:
            error_msg = serializer.errors[error_keys[0]]
            return Response({"message": error_msg[0]}, status=400)
        return Response(serializer.errors, status=400)


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer


class UserView(APIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = self.serializer_class(self.request.user).data
        data = {
            "status": "success",
            "message": f"Logged in User details for - {data.get('email')} retrieved successfully",
            "data": data,
        }
        return Response(data, status=status.HTTP_200_OK)
