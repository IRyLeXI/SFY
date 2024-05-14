from django.shortcuts import render
from .models import Playlist
from rest_framework.response import Response
from rest_framework import viewsets, status
from .serializers import PlaylistSerializer
from rest_framework.views import APIView
from SFY.firebase_utils import upload_playlist_picture_firebase

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
        
        
        
class UploadPictureView(APIView):
    def patch(self, request, pk, *args, **kwargs):
        try:
            playlist = Playlist.objects.get(pk=pk)
        except Playlist.DoesNotExist:
            return Response({'error': 'Playlist not found.'}, status=status.HTTP_404_NOT_FOUND)

        picture_file = request.FILES.get('picture')

        if not picture_file:
            return Response({'error': 'Picture file is required.'}, status=status.HTTP_400_BAD_REQUEST)

        firebase_url = upload_playlist_picture_firebase(picture_file)

        playlist.picture_url = firebase_url
        playlist.save()

        return Response({'detail': 'Playlist picture uploaded successfully.', 'firebase_url': firebase_url}, status=status.HTTP_201_CREATED)        