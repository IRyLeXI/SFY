from django.shortcuts import render
from .models import Author
from rest_framework.response import Response
from rest_framework import status, generics, viewsets, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action
from .serializers import AuthorSerializer
from SFY.permissions import IsSelfOrAdmin
from song.models import Song
from song.serializers import SongSerializer
from album.models import Album
from album.serializers import AlbumSerializer

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
    
    
    @action(detail=True, methods=['get'])
    def get_songs(self, request, pk=None):
        author = generics.get_object_or_404(Author, pk=pk)
        songs = Song.objects.filter(authors=author)
        serializer = SongSerializer(songs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'])
    def get_albums(self, request, pk=None):
        author = generics.get_object_or_404(Author, pk=pk)
        albums = Album.objects.filter(owner=author)
        serializer = AlbumSerializer(albums, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
        
        
    
    
    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # def perform_create(self, serializer):
    #     user = serializer.save()
    #     password = self.request.data.get('password')
    #     user.set_password(password)
    #     user.save()