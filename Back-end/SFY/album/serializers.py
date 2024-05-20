from rest_framework import serializers
from .models import Album
from author.models import Author

class AlbumSerializer(serializers.ModelSerializer):
    owner_username = serializers.SerializerMethodField()

    class Meta:
        model = Album
        fields = ['id', 'title', 'picture_url', 'created_date', 'publish_date', 'owner_id', 'owner_username', 'major_genre', 'songs', 'followers']

    def get_owner_username(self, obj):
        return obj.owner.username if obj.owner else None
