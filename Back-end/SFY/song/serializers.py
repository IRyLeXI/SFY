from rest_framework import serializers
from .models import Song
from author.models import Author

class SongSerializer(serializers.ModelSerializer):
    authors = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all(), many=True)
    
    class Meta:
        model = Song
        # fields = '__all__'
        fields = ['id', 'name', 'duration', 'listened_num', 'publication_date', 'audio_url', 'picture_url', 'authors']
        
    