from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from playlist.models import Playlist
from album.models import Album
from django.utils import timezone
from random import choice
from genre.models import Genre
from user.models import UserListens
from song.models import SongGenres

class FollowUnfollowMixin:
    @action(detail=True, methods=['post'])
    def follow(self, request, pk=None):
        user = request.user
        followed = self.get_object()
        
        if isinstance(followed, Album) and followed.publish_date > timezone.now():
            return Response({'error': 'You cannot follow this album as it has not been published yet'}, status=status.HTTP_403_FORBIDDEN)
        
        if isinstance(followed, Playlist) and followed.is_private:
            return Response({'error': 'You cannot follow this playlist as it is private'}, status=status.HTTP_403_FORBIDDEN)
        
        followed.followers.add(user)
        followed.save()
        
        return Response({'detail': 'Followed successfully'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['delete'])
    def unfollow(self, request, pk=None):
        user = request.user
        followed = self.get_object()

        if user.id == followed.owner.id:
            return Response({'error': 'You cannot unfollow yourself'}, status=status.HTTP_403_FORBIDDEN)

        if followed.followers.filter(id=user.id).exists():
            followed.followers.remove(user)
            followed.save()
            return Response({'detail': 'Unfollowed successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'You are not following this item'}, status=status.HTTP_400_BAD_REQUEST)


class FavoriteGenresMixin:
    def get_user_favorite_genres(self, user):
        user_listens = UserListens.objects.filter(user=user, is_slider_used=False)

        if not user_listens:
            random_genre_ids = [1, 2, 3]
            return Genre.objects.filter(id__in=random_genre_ids)[:3]

        genre_priority_sum = {}

        for listen in user_listens:
            genres = listen.song.genres.all()
            for genre in genres:
                original_priority = listen.song.songgenres_set.get(genre=genre).priority
                inverted_priority = 6 - original_priority
                genre_priority_sum[genre] = genre_priority_sum.get(genre, 0) + inverted_priority                    

        sorted_genres = sorted(genre_priority_sum, key=genre_priority_sum.get, reverse=True)
        print(sorted_genres)
        return sorted_genres[:10]
    
    def invert_priority(priority):
        return 6 - priority
    
    
    