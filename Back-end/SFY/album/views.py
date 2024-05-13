from django.shortcuts import render
from .models import Album
from rest_framework.response import Response
from rest_framework import status, generics, viewsets
from .serializers import AlbumSerializer

class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer