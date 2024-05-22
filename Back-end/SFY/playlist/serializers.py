from rest_framework import serializers
from .models import Playlist, PlaylistsSongs
from datetime import timedelta

class PlaylistSerializer(serializers.ModelSerializer):
    owner_username = serializers.SerializerMethodField()
    total_duration = serializers.SerializerMethodField()

    class Meta:
        model = Playlist
        fields = ['id', 'title', 'picture_url', 'created_date', 'updated_date', 'owner_id', 'owner_username', 'major_genre', 'is_private', 'is_generated', 'songs', 'followers', 'total_duration']

    def get_owner_username(self, obj):
        return obj.owner.username if obj.owner else None

    def get_total_duration(self, obj):
        total_duration_seconds = 0
        songs = obj.songs.all()
        for song in songs:
            total_duration_seconds += song.duration.total_seconds() if song.duration else 0
            
        total_duration = str(timedelta(seconds=total_duration_seconds))
        return total_duration
