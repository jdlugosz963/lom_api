from django.db.models.query import QuerySet
from django.http.response import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import generics
from rest_framework.views import Http404
from rest_framework.generics import get_object_or_404
from knox.auth import TokenAuthentication

from django.db.models.query import Q

from .models import *
from .serializers import *
from auth_api.serializers import UserSerializer


def set_users(request):
    users_list = request.data.get('users', [])
    user_pk = request.user.pk

    if isinstance(users_list, list):
        if user_pk not in users_list:
            users_list.append(user_pk)

    request.data['users'] = users_list

class GroupView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (TokenAuthentication, )
    serializer_class = GroupSerializer

    def get_queryset(self):
        return Group.objects.filter(
                    Q(owner=self.request.user) |
                    Q(users__in=(self.request.user.pk, ))
                ).distinct()
    
    def get_serializer_context(self):
        context = super(GroupView, self).get_serializer_context()
        context.update({"request": self.request})
        return context

    def create(self, request, *args, **kwargs):
        request.data['owner'] = request.user.pk
        set_users(request)
        return super().create(request, *args, **kwargs)

class GroupDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (TokenAuthentication, )
    serializer_class = GroupSerializer

    def get_queryset(self):
        return Group.objects.filter(
                    Q(owner=self.request.user)
                ).distinct()

    def get_serializer_context(self):
        context = super(GroupDetailView, self).get_serializer_context()
        context.update({"request": self.request})
        return context

    def update(self, request, *args, **kwargs):
        request.data['owner'] = request.user.pk
        set_users(request)

        return super().update(request, *args, **kwargs)

    def retrieve(self, request, pk):
        try:
            group = Group.objects.filter(
                Q(owner=request.user) |
                Q(users__in=(request.user.pk, ))
            ).distinct().get(Q(pk=pk))
        except Group.DoesNotExist:
            raise Http404

        serializer = GroupSerializer(group, context={"request": self.request})
        return Response(serializer.data)

class GmsView(APIView):
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (TokenAuthentication, )

    def get(self, request, pk):
        try:
            group = Group.objects.filter(
                Q(owner=request.user) |
                Q(users__in=(request.user.pk, ))
            ).distinct().get(Q(pk=pk))
        except Group.DoesNotExist:
            raise Http404

        serialzier = GroupMessagesSerializer(
            group, 
            context={"request": request}
        )
        
        return Response(serialzier.data)

    def post(self, request, pk):
        try: # check is user in group TODO: Make it better
            Group.objects.filter(
                Q(owner=request.user) |
                Q(users__in=(request.user.pk, ))
            ).distinct().get(Q(pk=pk))
        except Group.DoesNotExist:
            raise Http404

        request.data['sender'] = request.user.pk
        request.data['receiver'] = pk
        serializer = GmSimpleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        serializer = GmSerializer(serializer.instance)

        return Response(serializer.data)
