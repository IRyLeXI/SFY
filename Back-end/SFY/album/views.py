from django.shortcuts import render
from .models import Album
from rest_framework.response import Response
from rest_framework import status, generics, viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from .serializers import AlbumSerializer
from rest_framework.views import APIView
from SFY.firebase_utils import upload_album_picture_firebase
from SFY.permissions import IsAuthorOrAdmin, IsOwnerOrAdmin
from rest_framework.generics import get_object_or_404


class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    
    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [permissions.AllowAny]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsOwnerOrAdmin, permissions.IsAuthenticated]
        elif self.action == 'create':
            permission_classes = [IsAuthorOrAdmin, permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAuthenticated]
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
    
    
class UploadPictureView(APIView):
    permission_classes = [IsAuthenticated]
    
    def patch(self, request, pk, *args, **kwargs):
        album = get_object_or_404(Album, pk=pk)
        
        if request.user.id != album.owner.id:
            return Response({'error': 'You do not have permission to upload pictures to this album.'}, status=status.HTTP_403_FORBIDDEN)

        picture_file = request.FILES.get('picture')

        if not picture_file:
            return Response({'error': 'Picture file is required.'}, status=status.HTTP_400_BAD_REQUEST)

        firebase_url = upload_album_picture_firebase(picture_file)

        album.picture_url = firebase_url
        album.save()

        return Response({'detail': 'Album picture uploaded successfully.', 'firebase_url': firebase_url}, status=status.HTTP_200_OK)