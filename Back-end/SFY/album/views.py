from django.shortcuts import render
from .models import Album
from rest_framework.response import Response
from rest_framework import status, generics, viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404
from rest_framework.decorators import action
from rest_framework.views import APIView
from .serializers import AlbumSerializer
from SFY.firebase_utils import upload_album_picture_firebase
from SFY.permissions import IsAuthorOrAdmin, IsOwnerOrAdmin, IsAlbumPublishedOrAdmin
from SFY.mixins import FollowUnfollowMixin
from song.models import Song
from song.serializers import SongSerializer

class AlbumViewSet(viewsets.ModelViewSet, FollowUnfollowMixin):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    
    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy', 'add_song', 'add_songs']:
            permission_classes = [IsOwnerOrAdmin, permissions.IsAuthenticated]
        elif self.action == 'create':
            permission_classes = [IsAuthorOrAdmin, permissions.IsAuthenticated]
        elif self.action in ['retrieve', 'get_songs']:
            permission_classes = [IsAlbumPublishedOrAdmin]    
        elif self.action in ['follow', 'unfollow']:
            permission_classes = [permissions.IsAuthenticated]    
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]
    
    def create(self, request, *args, **kwargs):
        user = request.data.get('owner')
        request_user = request.user.id
        
        if user != request_user:
            return Response({'detail': 'You cannot create album for other user'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            album = serializer.save(owner_id=user)
            album.followers.add(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=True, methods=['get'])
    def get_songs(self, request, pk=None):
        album = self.get_object()
        songs = Song.objects.filter(albums=album)
        serializer = SongSerializer(songs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    @action(detail=True, methods=['post'],) 
    def add_song(self, request, pk=None):
        album = get_object_or_404(Album, pk=pk)
        
        if not IsOwnerOrAdmin().has_object_permission(request, self, album):
            return Response({'detail': 'You do not have permission to add songs to this album'}, status=status.HTTP_403_FORBIDDEN)
        
        song_id = request.data.get('song_id')
        album.songs.add(song_id)
        serializer = self.get_serializer(album)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def add_songs(self, request, pk=None):
        album = get_object_or_404(Album, pk=pk)
        
        if not IsOwnerOrAdmin().has_object_permission(request, self, album):
            return Response({'detail': 'You do not have permission to add songs to this album'}, status=status.HTTP_403_FORBIDDEN)
        
        song_ids = request.data.get('song_ids', [])
        
        if not isinstance(song_ids, list):
            raise Response({"error": "song_ids must be a list of integers."}, status=status.HTTP_400_BAD_REQUEST)
        
        songs = Song.objects.filter(pk__in=song_ids)
        
        if len(songs) != len(song_ids):
            return Response({'detail': 'One or more song IDs are invalid.'}, status=status.HTTP_400_BAD_REQUEST)
    
        for song in songs:
            album.songs.add(song)
        
        serializer = self.get_serializer(album)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class UploadPictureView(APIView):
    permission_classes = [IsAuthenticated]
    
    def patch(self, request, pk, *args, **kwargs):
        album = get_object_or_404(Album, pk=pk)
        
        if request.user.id != album.owner.id and not request.user.is_staff:
            return Response({'error': 'You do not have permission to upload pictures to this album.'}, status=status.HTTP_403_FORBIDDEN)

        picture_file = request.FILES.get('picture')

        if not picture_file:
            return Response({'error': 'Picture file is required.'}, status=status.HTTP_400_BAD_REQUEST)

        firebase_url = upload_album_picture_firebase(picture_file)

        album.picture_url = firebase_url
        album.save()

        return Response({'detail': 'Album picture uploaded successfully.', 'firebase_url': firebase_url}, status=status.HTTP_200_OK)