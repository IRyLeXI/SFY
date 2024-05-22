from rest_framework import serializers
from .models import Song, SongGenres, Genre
from author.models import Author

class SongSerializer(serializers.ModelSerializer):
    authors = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all(), many=True)
    authors_names = serializers.SerializerMethodField()
    
    class Meta:
        model = Song
        fields = ['id', 'name', 'duration', 'listened_num', 'publication_date', 'audio_url', 'picture_url', 'authors', 'authors_names']
        
    def get_authors_names(self, obj):
        return [author.username for author in obj.authors.all()]     
        

class SongGenresSerializer(serializers.ModelSerializer):
    genre_id = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all(), source='genre.id')
    priority = serializers.IntegerField()

    class Meta:
        model = SongGenres
        fields = ['genre_id', 'priority']