from django.shortcuts import render
from .models import Author
from rest_framework.response import Response
from rest_framework import status, generics, viewsets, permissions
from .serializers import AuthorSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from SFY.permissions import IsSelfOrAdmin

class AuthorViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    
    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsSelfOrAdmin, permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        user = serializer.save()
        password = self.request.data.get('password')
        user.set_password(password)
        user.save()