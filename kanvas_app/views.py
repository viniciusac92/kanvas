from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from kanvas_app.serializers import UserSerializer


class LoginView(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']

        user = authenticate(username=username, password=password)
        if user:
            import ipdb

            ipdb.set_trace()
            token = Token.objects.get_or_create(user=user)[0]
            return Response({'token': token.key})


class Accoutsview(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        if user != None:
            token = Token.objects.get_or_create(user=user)[0]
            return Response({'message': 'not protected'})
