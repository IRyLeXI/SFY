from rest_framework import serializers
from .models import CustomUser, UserListens

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = '__all__'


class UserListensSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserListens
        fields = '__all__'