from django.shortcuts import render
from .models import Playlist
from rest_framework.response import Response
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from .serializers import PlaylistSerializer
from SFY.firebase_utils import upload_playlist_picture_firebase
from SFY.permissions import IsOwnerOrAdmin, IsPlaylistPrivateOrAdmin
from SFY.mixins import FollowUnfollowMixin
from song.models import Song
from song.serializers import SongSerializer


class PlaylistViewSet(viewsets.ModelViewSet, FollowUnfollowMixin):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    
    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy', 'add_song']:
            permission_classes = [IsOwnerOrAdmin, permissions.IsAuthenticated]
        elif self.action in ['create', 'follow', 'unfollow']:
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['retrieve', 'get_songs']:
            permission_classes = [IsPlaylistPrivateOrAdmin]  
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]
    
    def create(self, request, *args, **kwargs):
        user = request.data.get('owner')
        request_user = request.user.id
        
        if user != request_user:
            return Response({'detail': 'You cannot create playlists for another user'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            playlist = serializer.save(owner_id=user)
            playlist.followers.add(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
    @action(detail=True, methods=['get'])
    def get_songs(self, request, pk=None):
        playlist = self.get_object()
        songs = Song.objects.filter(playlists=playlist)
        serializer = SongSerializer(songs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    @action(detail=True, methods=['post'],) 
    def add_song(self, request, pk=None):
        playlist = get_object_or_404(Playlist, pk=pk)
        
        if not IsOwnerOrAdmin().has_object_permission(request, self, playlist):
            return Response({'detail': 'You do not have permission to add songs to this playlist'}, status=status.HTTP_403_FORBIDDEN)
        
        song_id = request.data.get('song_id')
        playlist.songs.add(song_id)
        serializer = self.get_serializer(playlist)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
        
        
class UploadPictureView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def patch(self, request, pk, *args, **kwargs):
        playlist = get_object_or_404(Playlist, pk=pk)

        if request.user.id != playlist.owner.id and not request.user.is_staff:
            return Response({'error': 'You do not have permission to upload pictures to this playlist.'}, status=status.HTTP_403_FORBIDDEN)
        
        picture_file = request.FILES.get('picture')

        if not picture_file:
            return Response({'error': 'Picture file is required.'}, status=status.HTTP_400_BAD_REQUEST)

        firebase_url = upload_playlist_picture_firebase(picture_file)

        playlist.picture_url = firebase_url
        playlist.save()

        return Response({'detail': 'Playlist picture uploaded successfully.', 'firebase_url': firebase_url}, status=status.HTTP_201_CREATED)        