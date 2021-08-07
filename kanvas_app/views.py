from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from kanvas_app.models import Activity, Course, Submission
from kanvas_app.permissions import IsInstructorOrReadOnly, StudentOnly, TeamMemberOnly
from kanvas_app.serializers import (
    ActivitySimpleSerializer,
    ActivitySubmissionSerializer,
    CoursesSerializer,
    CoursesUserSerializer,
    SubmissionSerializer,
    SubmissionSimpleSerializer,
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
    permission_classes = [IsInstructorOrReadOnly]

    def get(self, _):
        courses = Course.objects.all()
        serialized = CoursesUserSerializer(courses, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

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

    def put(self, request, course_id):
        if course_id:
            try:
                user_ids_list = request.data['user_ids']
                students_list = []
                for student_id in user_ids_list:
                    user = get_object_or_404(User, id=student_id)
                    if user and not user.is_staff and not user.is_superuser:
                        students_list.append(user)

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


class CoursesRetrieveView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsInstructorOrReadOnly]

    def get(self, _, course_id):
        if course_id:
            try:
                selected_course = Course.objects.get(id=course_id)
                course_serialized = CoursesUserSerializer(selected_course)
                return Response(course_serialized.data, status=status.HTTP_200_OK)

            except ObjectDoesNotExist:
                return Response(
                    {"errors": "invalid course_id"}, status=status.HTTP_404_NOT_FOUND
                )

    def delete(self, _, course_id):
        course = get_object_or_404(Course, id=course_id)
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ActivitiesView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [TeamMemberOnly]

    def get(self, _):
        activities = Activity.objects.all()
        for activity_data in activities:
            submissions = Submission.objects.filter(activity_id=activity_data.id)
            submission_list = []
            for sub in submissions:
                submission_list.append(sub)
            activity_data.submissions.set(submission_list)

        serialized = ActivitySubmissionSerializer(activities, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def post(self, request):
        activity_request_serializer = ActivitySimpleSerializer(data=request.data)

        if not activity_request_serializer.is_valid():
            return Response(
                activity_request_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        validated_activity_data = activity_request_serializer.validated_data
        activity_request_data = Activity.objects.get_or_create(
            **validated_activity_data
        )[0]
        activity_request_data.submissions.set([])
        retrieve_serializer = ActivitySubmissionSerializer(activity_request_data)
        return Response(retrieve_serializer.data, status=status.HTTP_201_CREATED)


class SubmissionView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [StudentOnly]

    def post(self, request, activity_id):
        if activity_id:
            try:
                submission_request_serializer = SubmissionSimpleSerializer(
                    data=request.data
                )
                if not submission_request_serializer.is_valid():
                    return Response(
                        submission_request_serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                validated_activity_data = submission_request_serializer.validated_data
                submission_create_data = Submission(
                    grade=None,
                    repo=validated_activity_data['repo'],
                    user_id=request.user.id,
                    activity_id=activity_id,
                )
                submission_create_data.save()
                retrieve_submission_serialized = SubmissionSerializer(
                    submission_create_data
                )
                return Response(
                    retrieve_submission_serialized.data, status=status.HTTP_201_CREATED
                )

            except ObjectDoesNotExist:
                return Response(
                    {'message': 'Id not found'}, status=status.HTTP_404_NOT_FOUND
                )


class SubmissionEditView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [TeamMemberOnly]

    def put(self, request, submission_id):
        if submission_id:
            try:
                student_grade = request.data['grade']
                submission_selected_data = get_object_or_404(
                    Submission, id=submission_id
                )
                submission_selected_data.grade = student_grade
                submission_selected_data.save()
                retrieve_submission_serialized = SubmissionSerializer(
                    submission_selected_data
                )
                return Response(
                    retrieve_submission_serialized.data, status=status.HTTP_200_OK
                )

            except ObjectDoesNotExist:
                return Response(
                    {'message': 'Id not found'}, status=status.HTTP_404_NOT_FOUND
                )


class SubmissionRetrieveView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.is_staff:
            submissions = Submission.objects.filter(user_id=request.user.id)
            serialized = SubmissionSerializer(submissions, many=True)
            return Response(serialized.data, status=status.HTTP_200_OK)
        submissions = Submission.objects.all()
        serialized = SubmissionSerializer(submissions, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)
