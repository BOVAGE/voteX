from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer as JwtTokenObtainPairSerializer
from rest_framework.exceptions import APIException
from .models import CustomUser, Student, Guest

print(get_user_model())
class APIException400(APIException):
    status_code = 400



class TokenObtainPairSerializer(JwtTokenObtainPairSerializer):
    # username_field = get_user_model().USERNAME_FIELD
    pass


class UserSerializer(serializers.ModelSerializer):
    matric_no = serializers.CharField(required=False)
    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'username', 'user_type', 'matric_no', 'phone_number',)

    def validate(self, data):
        email = data.get('email')
        username = data.get('username')
        phone_number = data.get('phone_number')
        user_type = data.get('user_type')
        matric_no = data.get('matric_no')

        if not email:
            raise APIException400({"message": "email is required"})
        if not username:
            raise APIException400({"message": "username is required"})
        if not phone_number:
            raise APIException400({"message": "phone number is required"})
        if CustomUser.objects.filter(email=email).exists():
            raise APIException400({"message": "This email already exists. Please login"})

        # Check if user_type is 'student' and matric_no is not provided
        if user_type == 'student' and not matric_no:
            raise serializers.ValidationError("Matric number must be supplied for student user type.")

        return data
    def create(self, validated_data):

        email = validated_data['email']
        username = validated_data['username']
        phone_number = validated_data['phone_number']
        user_type = validated_data.get('user_type')
        matric_no = validated_data.get('matric_no')
        password = validated_data.get("password")
        user = CustomUser.objects.create_user(email=email, phone_number=phone_number, username=username, user_type=user_type, password=password)
        if user_type=='student':
            student_obj = Student.objects.create(user=user, matric_no=matric_no)
        else:
            guest_obj = Guest.objects.create(user=user)

        
      
        
        return validated_data