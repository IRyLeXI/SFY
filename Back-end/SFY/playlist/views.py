from django.shortcuts import render
from .models import Playlist
from rest_framework.response import Response
from rest_framework import viewsets, status, permissions
from .serializers import PlaylistSerializer
from rest_framework.views import APIView
from SFY.firebase_utils import upload_playlist_picture_firebase
from rest_framework.generics import get_object_or_404
from SFY.permissions import IsOwnerOrAdmin

class PlaylistViewSet(viewsets.ModelViewSet):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    
    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [permissions.AllowAny]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsOwnerOrAdmin, permissions.IsAuthenticated]
        elif self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def create(self, request, *args, **kwargs):
        user = request.data.get('owner')
        request_user = request.user.id
        
        if user != request_user:
            return Response({'detail': 'You cannot create playlists for other user'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            playlist = serializer.save(owner_id=user)
            playlist.followers.add(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
        
class UploadPictureView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def patch(self, request, pk, *args, **kwargs):
        playlist = get_object_or_404(Playlist, pk=pk)

        if request.user.id != playlist.owner.id:
            return Response({'error': 'You do not have permission to upload pictures to this playlist.'}, status=status.HTTP_403_FORBIDDEN)
        
        picture_file = request.FILES.get('picture')

        if not picture_file:
            return Response({'error': 'Picture file is required.'}, status=status.HTTP_400_BAD_REQUEST)

        firebase_url = upload_playlist_picture_firebase(picture_file)

        playlist.picture_url = firebase_url
        playlist.save()

        return Response({'detail': 'Playlist picture uploaded successfully.', 'firebase_url': firebase_url}, status=status.HTTP_201_CREATED)        