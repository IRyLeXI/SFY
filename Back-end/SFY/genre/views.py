from django.shortcuts import render
from .models import Genre
from rest_framework.response import Response
from rest_framework import status, generics, viewsets, permissions
from .serializers import GenreSerializer

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]