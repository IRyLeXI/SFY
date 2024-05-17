from rest_framework import serializers
from .models import Song, SongGenres, Genre
from author.models import Author

class SongSerializer(serializers.ModelSerializer):
    authors = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all(), many=True)
    
    class Meta:
        model = Song
        # fields = '__all__'
        fields = ['id', 'name', 'duration', 'listened_num', 'publication_date', 'audio_url', 'picture_url', 'authors']
        

class SongGenresSerializer(serializers.ModelSerializer):
    genre_id = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all(), source='genre.id')
    priority = serializers.IntegerField()

    class Meta:
        model = SongGenres
        fields = ['genre_id', 'priority']