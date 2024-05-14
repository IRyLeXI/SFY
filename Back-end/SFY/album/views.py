from django.shortcuts import render
from .models import Album
from rest_framework.response import Response
from rest_framework import status, generics, viewsets
from .serializers import AlbumSerializer
from rest_framework.views import APIView
from SFY.firebase_utils import upload_album_picture_firebase

class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    
    
    
class UploadPictureView(APIView):
    def patch(self, request, pk, *args, **kwargs):
        try:
            album = Album.objects.get(pk=pk)
        except Album.DoesNotExist:
            return Response({'error': 'Album not found.'}, status=status.HTTP_404_NOT_FOUND)

        picture_file = request.FILES.get('picture')

        if not picture_file:
            return Response({'error': 'Picture file is required.'}, status=status.HTTP_400_BAD_REQUEST)

        firebase_url = upload_album_picture_firebase(picture_file)

        album.picture_url = firebase_url
        album.save()

        return Response({'detail': 'Album picture uploaded successfully.', 'firebase_url': firebase_url}, status=status.HTTP_200_OK)
