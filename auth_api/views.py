from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http.response import Http404
from django.shortcuts import get_object_or_404

from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

from knox.views import LoginView as KnoxLoginView
from knox.auth import TokenAuthentication

from .serializers import UserSerializer, RegisterUserSerializer

class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request):
        token_serializer = AuthTokenSerializer(data=request.data)
        token_serializer.is_valid(raise_exception=True)
        user = token_serializer.validated_data['user']

        user_serializer = UserSerializer(user)

        login(request, user)
        
        response = super(LoginView, self).post(request, format=None)
        response.data['user'] = user_serializer.data

        return Response(response.data, status=200)

class RegisterView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.register_user()

        return Response(status=200)

class UserInfo(APIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request):
        user = request.GET.get("pk", request.user)
        username = request.GET.get("username", None)

        if username:
            users = User.objects.filter(username__startswith = username)[:5]
            serializer = UserSerializer(users, many=True)

            return Response({
                "users": serializer.data 
            })

        if not isinstance(user, User):
            try:
                user = get_object_or_404(User, pk=user)
            except ValueError:
                raise Http404
        
        serializer = UserSerializer(user)
        
        return Response({
            "user": serializer.data
        })