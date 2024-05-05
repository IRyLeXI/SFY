from django.shortcuts import render
from .models import Song
from rest_framework.response import Response
from rest_framework import status, generics, viewsets
from .serializers import SongSerializer

class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer