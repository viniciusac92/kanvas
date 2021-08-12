from rest_framework import serializers
from traitlets.traitlets import default


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    is_staff = serializers.BooleanField(required=False)
    is_superuser = serializers.BooleanField(required=False)


class UserSimpleSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()


class CoursesSerializer(serializers.Serializer):
    name = serializers.CharField()


class CoursesUserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    users = UserSimpleSerializer(many=True)


class SubmissionSimpleSerializer(serializers.Serializer):
    grade = serializers.IntegerField(read_only=True, default=None)
    repo = serializers.CharField()


class SubmissionSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    grade = serializers.IntegerField()
    repo = serializers.CharField()
    user_id = serializers.IntegerField()
    activity_id = serializers.IntegerField()


class ActivitySubmissionSerializer(serializers.Serializer):
    id = serializers.IntegerField(default=None)
    title = serializers.CharField()
    points = serializers.IntegerField()


class ActivitySubmissionResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    points = serializers.IntegerField()
    submissions = SubmissionSerializer(many=True, default=[])
