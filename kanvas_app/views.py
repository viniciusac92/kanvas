from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from kanvas_app.models import Course
from kanvas_app.permissions import IsInstructor
from kanvas_app.serializers import (
    CoursesSerializer,
    CoursesUserSerializer,
    UserSerializer,
    UserSimpleSerializer,
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
    def get(self, _):
        courses = Course.objects.all()
        serialized = CoursesUserSerializer(courses, many=True)

        return Response(serialized.data, status=status.HTTP_200_OK)

    @authentication_classes([TokenAuthentication])
    @permission_classes([IsAuthenticated, IsInstructor])
    def post(self, request):
        course_request_serializer = CoursesSerializer(data=request.data)

        if not course_request_serializer.is_valid():
            return Response(
                course_request_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        validated_course_data = course_request_serializer.validated_data
        course_request_data = Course.objects.get_or_create(**validated_course_data)[0]
        course_request_data.users.set([])
        retrieve_serializer = CoursesUserSerializer(course_request_data)

        return Response(retrieve_serializer.data, status=status.HTTP_201_CREATED)

    @authentication_classes([TokenAuthentication])
    @permission_classes([IsAuthenticated, IsInstructor])
    def put(self, request, course_id):
        if course_id:
            try:
                user_ids_list = request.data['user_ids']
                students_list = []

                for student_id in user_ids_list:
                    user = User.objects.get(id=student_id)
                    if user and not user.is_staff and not user.is_superuser:
                        students_list.append(user)

                    else:
                        return Response(
                            {'errors': 'Only students can be enrolled in the course.'},
                            status=status.HTTP_400_BAD_REQUEST,
                        )

                course_selected_data = Course.objects.get(id=course_id)
                if not course_selected_data:
                    return Response(
                        {"errors": "invalid course_id"},
                        status=status.HTTP_404_NOT_FOUND,
                    )
                course_selected_data.users.set(students_list)
                retrieve_course_serialized = CoursesUserSerializer(course_selected_data)

                return Response(
                    retrieve_course_serialized.data, status=status.HTTP_200_OK
                )

            except ObjectDoesNotExist:
                return Response(
                    {'message': 'Id not found'}, status=status.HTTP_404_NOT_FOUND
                )
