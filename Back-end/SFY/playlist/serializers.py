from rest_framework import serializers
from .models import Playlist

class PlaylistSerializer(serializers.ModelSerializer):
    created_date = serializers.DateField(format='%Y-%m-%d', required=False)
    updated_date = serializers.DateField(format='%Y-%m-%d', required=False)
    
    
    class Meta:
        model = Playlist
        fields = '__all__'
