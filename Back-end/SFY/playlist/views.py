from django.shortcuts import render
from .models import Playlist
from rest_framework.response import Response
from rest_framework import viewsets, status
from .serializers import PlaylistSerializer

# Create your views here.
class PlaylistViewSet(viewsets.ModelViewSet):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    
    def create(self, request, *args, **kwargs):
        user = request.data.get('owner')

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            playlist = serializer.save(owner_id=user)
            playlist.followers.add(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)