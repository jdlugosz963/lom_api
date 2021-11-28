from django.db.models import fields
from rest_framework import serializers
from .models import *

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
