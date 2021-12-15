from django.db.models import fields
from django.contrib.auth.models import User

from rest_framework import serializers
from .models import *
from auth_api.serializers import UserSerializer

class GroupSerializer(serializers.ModelSerializer):
    is_mine = serializers.SerializerMethodField('_is_mine')

    def _is_mine(self, obj):
        request = self.context.get('request')
        if request:
            return request.user == obj.owner
        return False

    class Meta:
        model = Group
        fields = '__all__'
        extra_fields = ('is_mine', )

class DmSerializer(serializers.ModelSerializer):
    is_mine = serializers.SerializerMethodField('_is_mine')

    def _is_mine(self, obj):
        request = self.context.get('request')
        if request:
            return request.user == obj.sender
        return False
    class Meta:
        model = Dm
        fields = '__all__'

class GmSerializer(serializers.ModelSerializer):
    is_mine = serializers.SerializerMethodField('_is_mine')
    sender = UserSerializer(read_only=True)

    def _is_mine(self, obj):
        request = self.context.get('request')
        if request:
            return request.user == obj.sender
        return False
    class Meta:
        model = Gm
        fields = '__all__'

class GroupMessagesSerializer(serializers.ModelSerializer):
    messages = serializers.SerializerMethodField('_messages')

    def _messages(self, obj):
        request = self.context.get('request')
        if request:
            gms = GmSerializer(obj.receiver_gm.all(), many=True, read_only=True, context={"request": request})
            return gms.data
        return []

    class Meta:
        model=Group
        fields=('messages', )
