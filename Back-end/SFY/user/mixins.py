from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from user.models import CustomUser
from song.models import Song
from author.models import Author
from album.models import Album
from playlist.models import Playlist
from user.serializers import UserSerializer
from song.serializers import SongSerializer
from author.serializers import AuthorSerializer
from album.serializers import AlbumSerializer
from playlist.serializers import PlaylistSerializer

class SearchMixin:
    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('query', '')
        if not query:
            return Response({'error': 'Query parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)

        songs = Song.objects.filter(name__istartswith=query)
        authors = Author.objects.filter(username__istartswith=query)
        albums = Album.objects.filter(title__istartswith=query)
        playlists = Playlist.objects.filter(title__istartswith=query)
        users = CustomUser.objects.filter(username__istartswith=query, is_author=False)

        song_serializer = SongSerializer(songs, many=True)
        author_serializer = AuthorSerializer(authors, many=True)
        album_serializer = AlbumSerializer(albums, many=True)
        playlist_serializer = PlaylistSerializer(playlists, many=True)
        user_serializer = UserSerializer(users, many=True)

        return Response({
            'songs': song_serializer.data,
            'authors': author_serializer.data,
            'albums': album_serializer.data,
            'playlists': playlist_serializer.data,
            'users': user_serializer.data,
        }, status=status.HTTP_200_OK)
