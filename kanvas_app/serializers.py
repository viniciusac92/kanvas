from rest_framework import serializers


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


class SubmissionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    grade = serializers.IntegerField()
    repo = serializers.CharField()
    user_id = serializers.IntegerField()
    activity_id = serializers.IntegerField()


class ActivitySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    points = serializers.IntegerField()
    submissions = SubmissionSerializer(many=True)
