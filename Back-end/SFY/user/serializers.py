from rest_framework import serializers
from .models import CustomUser, UserListens

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        exclude = ['listens', 'user_permissions', 'groups', 'is_staff', 'is_active', 'date_joined']


class UserListensSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserListens
        fields = '__all__'