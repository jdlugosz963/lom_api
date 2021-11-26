from django.db.models.query import QuerySet
from django.http.response import Http404
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import generics
from knox.auth import TokenAuthentication

from django.db.models.query import Q

from .models import *
from .serializers import *

class GroupView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (TokenAuthentication, )
    serializer_class = GroupSerializer

    def get_queryset(self):
        return Group.objects.filter(
                    Q(owner=self.request.user) |
                    Q(users__in=(self.request.user, ))
                ).distinct()

    def create(self, request, *args, **kwargs):
        request.data['owner'] = request.user.pk
        return super().create(request, *args, **kwargs)