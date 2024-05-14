from django.shortcuts import render
from .models import CustomUser
from rest_framework.response import Response
from rest_framework import status, generics, viewsets
from .serializers import UserSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from SFY.firebase_utils import upload_to_firebase_storage


class UserViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        user = serializer.save()
        password = self.request.data.get('password')
        user.set_password(password)
        user.save()


class UploadPictureView(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user

        picture_file = request.FILES.get('picture')

        if not picture_file:
            return Response({'error': 'Picture file is required.'}, status=status.HTTP_400_BAD_REQUEST)

        firebase_url = upload_to_firebase_storage(picture_file)

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