from django.shortcuts import render
from .models import CustomUser
from rest_framework.response import Response
from rest_framework import status, generics, viewsets, permissions
from .serializers import UserSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from SFY.firebase_utils import upload_user_picture_firebase
from SFY.permissions import IsSelfOrAdmin
from rest_framework.generics import get_object_or_404


class UserViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsSelfOrAdmin, permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]
    

class UploadPictureView(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user

        picture_file = request.FILES.get('picture')

        if not picture_file:
            return Response({'error': 'Picture file is required.'}, status=status.HTTP_400_BAD_REQUEST)

        firebase_url = upload_user_picture_firebase(picture_file)

        user.firebase_profile_picture_url = firebase_url
        user.save()

        return Response({'detail': 'Profile picture uploaded successfully.', 'firebase_url': firebase_url}, status=status.HTTP_201_CREATED)

# class UserAPIList(generics.ListCreateAPIView):
#     queryset = CustomUser.objects.all()
#     serializer_class = UserSerializer
    
# class UserAPIUpdate(generics.UpdateAPIView):
#     queryset = CustomUser.objects.all()
#     serializer_class = UserSerializer
    
# class UserAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = CustomUser.objects.all()
#     serializer_class = UserSerializer