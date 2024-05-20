from django.shortcuts import render
from django.utils.dateparse import parse_duration
from .models import CustomUser, UserListens, UserFollowers
from genre.models import Genre
from song.models import Song
from playlist.models import Playlist
from playlist.serializers import PlaylistSerializer
from album.models import Album
from album.serializers import AlbumSerializer
from rest_framework.response import Response
from rest_framework import status, generics, viewsets, permissions
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.decorators import action
from .serializers import UserSerializer, UserListensSerializer
from .mixins import SearchMixin
from SFY.firebase_utils import upload_user_picture_firebase
from SFY.permissions import IsSelfOrAdmin
from SFY.mixins import FavoriteGenresMixin


class UserViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy',]:
            permission_classes = [IsSelfOrAdmin, permissions.IsAuthenticated]
        elif self.action in ['follow', 'unfollow', 'is_logged_in', 'get_user_followed_albums_playlists']:
            permission_classes = [permissions.IsAuthenticated]    
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]
    
    
    @action(detail=True, methods=['post'])
    def follow(self, request, pk=None):
        user = request.user
        followed = get_object_or_404(CustomUser, pk=pk)

        if user.id == followed.id:
            return Response({'error': 'You cannot follow yourself'}, status=status.HTTP_403_FORBIDDEN)
        
        followed.followers.add(user)
        followed.save()
        
        return Response({'detail': 'Followed successfully'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['delete'])
    def unfollow(self, request, pk=None):
        user = request.user
        followed = get_object_or_404(CustomUser, pk=pk)

        if user.id == followed.id:
            return Response({'error': 'You cannot unfollow yourself'}, status=status.HTTP_403_FORBIDDEN)

        if followed.followers.filter(id=user.id).exists():
            followed.followers.remove(user)
            followed.save()
            return Response({'detail': 'Unfollowed successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'You are not following this user'}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=True, methods=['get'])    
    def get_user_playlists(self, request, pk=None):
        if request.user.is_authenticated and request.user.id==pk:
            print("auth")
            playlists = Playlist.objects.filter(owner=pk, is_generated=False)
        else:
            print("unauth")
            playlists = Playlist.objects.filter(owner=pk, is_private = False, is_generated=False)      
        serializer = PlaylistSerializer(playlists, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'])    
    def get_user_followed_to(self, request, pk=None):
        followed_users_ids = UserFollowers.objects.filter(follower_id=pk).values_list('user_id', flat=True)
        followed_users = CustomUser.objects.filter(id__in=followed_users_ids)
        serializer = UserSerializer(followed_users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'])
    def get_user_followed_albums_playlists(self, request):
        user = request.user
        
        favourite_playlist = Playlist.objects.filter(owner=user, title="Liked songs").first()
        favourite_serializer = PlaylistSerializer(favourite_playlist)
        
        subscribed_albums = Album.objects.filter(followers=user)
        album_serializer = AlbumSerializer(subscribed_albums, many=True)
        
        subscribed_playlists = Playlist.objects.filter(followers=user, is_generated=False)
        playlist_serializer = PlaylistSerializer(subscribed_playlists, many=True)
        
        return Response({
            'liked_songs': favourite_serializer.data,
            'subscribed_albums': album_serializer.data,
            'subscribed_playlists': playlist_serializer.data
        }, status=status.HTTP_200_OK)    
    
    
    @action(detail=True, methods=['get'])    
    def is_logged_in(self, request):
        return Response(request.user.id, status=status.HTTP_200_OK)
        
        
class UploadPictureView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        user = request.user

        picture_file = request.FILES.get('picture')

        if not picture_file:
            return Response({'error': 'Picture file is required.'}, status=status.HTTP_400_BAD_REQUEST)

        firebase_url = upload_user_picture_firebase(picture_file)

        user.picture_url = firebase_url
        user.save()

        return Response({'detail': 'Profile picture uploaded successfully.', 'firebase_url': firebase_url}, status=status.HTTP_201_CREATED)



class UserRecommendations(viewsets.ViewSet, FavoriteGenresMixin, SearchMixin):
    def get_permissions(self):
        if self.action in ['get_user_favorite_genre']:        
            permission_classes = [permissions.IsAuthenticated]    
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['get'])
    def get_user_favorite_genre(self, request):
        user = request.user
        top_genres = self.get_user_favorite_genres(user)
        genre_data = [self.serialize_genre(genre) for genre in top_genres]
        return Response({'top_genres': genre_data}, status=status.HTTP_200_OK)
    
    def serialize_genre(self, genre):
        return {
            'id': genre.id,
            'name': genre.name,
        }
    
    
class UserListen(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=True, methods=['post'])
    def listen(self, request):
        user = request.user
        song_id = request.data.get('song_id')

        if not song_id:
            return Response({'error': 'Song ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        song = get_object_or_404(Song, id=song_id)

        listen_time = request.data.get('listen_time')
        is_slider_used = request.data.get('is_slider_used', False)
        slider_stamp = request.data.get('slider_stamp')

        listen = UserListens.objects.create(
            user=user,
            song=song,
            listen_time=listen_time,
            is_slider_used=is_slider_used,
            slider_stamp=slider_stamp
        )
        
        song.listened_num += 1
        song.save()

        serializer = UserListensSerializer(listen)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
       
        
    @action(detail=True, methods=['get'])  
    def get_by_song(self, request, pk=None): #pk is song id
        user = request.user
        instance = get_object_or_404(UserListens, user=user, song=pk, listen_time=None)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    
    @action(detail=True, methods=['patch'])      
    def patch_song_listen(self, request, pk=None):
        listen = get_object_or_404(UserListen, pk=pk)
        serializer = self.get_serializer(listen, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)        
    
    
    @action(detail=True, methods=['patch'])
    def stop_last_listen(self, request):
        user = request.user
        duration = request.data.get('duration')

        if not duration:
            return Response({'error': 'Duration is required.'}, status=status.HTTP_400_BAD_REQUEST)

        last_listen = get_object_or_404(UserListens, user=user, listen_time=None)

        listen_time = parse_duration(duration)
        if not listen_time:
            return Response({'error': 'Invalid duration format. Use HH:MM:SS.'}, status=status.HTTP_400_BAD_REQUEST)

        if last_listen.is_slider_used:
            slider_stamp = parse_duration(last_listen.slider_stamp)
            if not slider_stamp:
                return Response({'error': 'Invalid slider stamp format.'}, status=status.HTTP_400_BAD_REQUEST)
            
            listen_time -= slider_stamp

        last_listen.listen_time = listen_time
        last_listen.save()

        serializer = UserListensSerializer(last_listen)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    