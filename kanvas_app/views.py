from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from kanvas_app.models import Courses
from kanvas_app.permissions import IsInstructor
from kanvas_app.serializers import (
    CoursesSerializer,
    CoursesUserSerializer,
    UserSerializer,
)


class LoginView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password'],
        )
        if user:
            token = Token.objects.get_or_create(user=user)[0]

            return Response({'token': token.key}, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_401_UNAUTHORIZED)


class AccountsView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=serializer.validated_data['username']).exists():
            return Response(
                {'error': 'username already exists'},
                status=status.HTTP_409_CONFLICT,
            )

        new_user = User.objects.create_user(**serializer.validated_data)
        serializer_to_retrieve = UserSerializer(new_user)

        return Response(serializer_to_retrieve.data)


class CoursesView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsInstructor]

    def post(self, request):
        course_request_serializer = CoursesSerializer(data=request.data)

        if not course_request_serializer.is_valid():
            return Response(
                course_request_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        validated_course_data = course_request_serializer.validated_data
        course_request_data = Courses.objects.get_or_create(**validated_course_data)[0]
        course_request_data.users.set([])
        retrieve_serializer = CoursesUserSerializer(course_request_data)

        return Response(retrieve_serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request):
        return Response({'msg': 'Put OK'})
