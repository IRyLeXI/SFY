from django.shortcuts import render
from datetime import timedelta
from django.utils import timezone
from django.db.models import Count
from .models import Playlist
from rest_framework.response import Response
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from .serializers import PlaylistSerializer
from SFY.firebase_utils import upload_playlist_picture_firebase
from SFY.permissions import IsOwnerOrAdmin, IsPlaylistPrivateOrAdmin
from SFY.mixins import FollowUnfollowMixin, FavoriteGenresMixin
from song.models import Song
from song.serializers import SongSerializer
from genre.models import Genre
from user.models import CustomUser
from random import shuffle, choices

class PlaylistViewSet(viewsets.ModelViewSet, FollowUnfollowMixin):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    
    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy', 'add_song']:
            permission_classes = [IsOwnerOrAdmin, permissions.IsAuthenticated]
        elif self.action in ['create', 'follow', 'unfollow', 'get_daily_playlists']:
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
        song = get_object_or_404(Song, pk=song_id)
        playlist.songs.add(song)
        
        playlist.updated_date = timezone.now()
        playlist.save()
        
        playlist.set_major_genre('playlists')
        serializer = self.get_serializer(playlist)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    @action(detail=True, methods=['get'])
    def get_global_playlists(self, request):        
        global_playlists = Playlist.objects.filter(owner_id=1, is_private=False)
        serializer = self.get_serializer(global_playlists, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'])  
    def get_daily_playlists(self, request):
        user_id = request.user.id
        user_playlists = Playlist.objects.filter(owner_id=user_id, title__startswith='Daily Recommendations', is_generated=True)
        serializer = PlaylistSerializer(user_playlists, many=True)
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
    
    
    
class PlaylistGenerators(viewsets.ViewSet, FavoriteGenresMixin):
    def get_permissions(self):
        if self.action in ['update_admin_playlists']:
            permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated] 
        return [permission() for permission in permission_classes]
    
    @action(detail=True, methods=['get'])
    def get_daily_playlist(self, request, pk=None):
        playlist = get_object_or_404(Playlist, pk=pk)

        if not playlist.owner == request.user:
            return Response({'error': 'Not allowed'}, status=status.HTTP_403_FORBIDDEN)
        
        if not playlist.is_generated:
            return Response({'detail': 'This playlist is not generated automatically.'}, status=status.HTTP_400_BAD_REQUEST)

        now = timezone.now()
        if playlist.updated_date and (now - playlist.updated_date) < timedelta(hours=24) and playlist.major_genre:
            return self._get_existing_songs_response(playlist)
        
        playlists = Playlist.objects.filter(owner=playlist.owner, title__in=[
            'Daily Recommendations 1', 'Daily Recommendations 2', 'Daily Recommendations 3'
        ])
        
        favorite_genres = self.get_user_favorite_genres(playlist.owner)[:3]
        
        if len(favorite_genres) < 3:
            available_genres = Genre.objects.filter(id__in=[1, 2, 3])
            missing_genres = 3 - len(favorite_genres)
            favorite_genres += choices(available_genres, k=missing_genres)
            
        shuffle(favorite_genres)

        print(favorite_genres)
        
        for pl in playlists:
            self._clear_playlist(pl)
            self._generate_songs_for_playlist(pl, favorite_genres.pop(0))
            pl.updated_date = now
            pl.save()

        return self._get_existing_songs_response(playlist)


    @action(detail=False, methods=['post'])
    def update_admin_playlists(self, request):
        admin_user = get_object_or_404(CustomUser, pk=1)
        playlist_titles = ['Pop', 'Rock', 'Hip-Hop', 'Electro', 'Indie', 'R&b', 'Classic']
        
        playlists = Playlist.objects.filter(owner=admin_user, title__in=playlist_titles)
        
        for pl in playlists:
            genre_name = pl.title
            genre = get_object_or_404(Genre, name=genre_name)
            
            self._clear_playlist(pl)
            self._generate_songs_for_playlist(pl, genre)
            pl.updated_date = timezone.now()
            pl.save()
        
        return Response({'detail': 'Admin playlists updated successfully.'}, status=status.HTTP_200_OK)
    
    
    @action(detail=True, methods=['post'])
    def generate_playlist_from_song(self, request):
        song_id = request.data.get('song_id')
        
        song = get_object_or_404(Song, pk=song_id)
        
        song_genres = song.genres.all()
        
        helper_playlist = Playlist.objects.get(owner=request.user, title="Helper playlist")
        helper_playlist.songs.clear()
        
        if len(song_genres) < 3:
            similar_songs = Song.objects.filter(genres__in=song_genres)
        else:
            similar_songs = Song.objects.filter(genres__in=song_genres).annotate(genre_count=Count('genres')).filter(genre_count__gte=3)
        similar_songs = similar_songs.order_by('-listened_num')
        
        for song in similar_songs:
            helper_playlist.songs.add(song)
        
        if helper_playlist.songs.count() < 30:
            similar_songs = Song.objects.filter(genres__in=song_genres).annotate(genre_count=Count('genres')).filter(genre_count=1)
            similar_songs = similar_songs.order_by('-listened_num')
            
            for song in similar_songs:
                helper_playlist.songs.add(song)
        
        return self._get_existing_songs_response(helper_playlist)


    def _generate_songs_for_playlist(self, playlist, genre):
        genre_songs = Song.objects.filter(genres=genre)
        song_scores = {}
        total_score = 0
        for song in genre_songs:
            priority = song.songgenres_set.get(genre=genre).priority
            score = song.listened_num * (1 - ((priority - 1) * 1.5 / 10))
            song_scores[song] = score
            total_score+=score
        
        if len(genre_songs) < 30:
            chosen_songs = sorted(song_scores, key=song_scores.get, reverse=True)[:30]     
        else:              
            probabilities = [score / total_score for score in song_scores.values()]
            chosen_songs = choices(list(song_scores.keys()), weights=probabilities, k=30)
        
        playlist.songs.add(*chosen_songs)
        playlist.major_genre = genre
        playlist.updated_date = timezone.now()
        playlist.save()



    def _clear_playlist(self, playlist):
        playlist.songs.clear()
        playlist.major_genre = None

    def _get_existing_songs_response(self, playlist):
        songs = playlist.songs.all()
        serializer = SongSerializer(songs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)