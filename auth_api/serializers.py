from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'is_staff')

class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        

    def register_user(self):
        user = User.objects.create_user(
            username = self.validated_data['username'],
            password = self.validated_data['password']
        )

        return user