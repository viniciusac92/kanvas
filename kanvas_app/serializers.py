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


class CoursesUserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    users = UserSimpleSerializer(many=True)
