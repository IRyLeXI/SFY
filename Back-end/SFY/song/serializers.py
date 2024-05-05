from rest_framework import serializers
from .models import Song
from author.models import Author
from playlist.models import Playlist

class SongSerializer(serializers.ModelSerializer):
    authors = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all(), many=True)
    playlists = serializers.PrimaryKeyRelatedField(queryset=Playlist.objects.all(), many=True)
    
    class Meta:
        model = Song
        # fields = '__all__'
        fields = ['id', 'name', 'duration', 'listened_num', 'publication_date', 'picture', 'authors', 'playlists']
        
    