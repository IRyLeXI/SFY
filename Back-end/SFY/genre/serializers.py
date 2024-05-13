from rest_framework import serializers
from .models import Genre

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'
        
        
    def create(self, validated_data):
        validated_data['name'] = validated_data['name'].lower().capitalize()
        return super().create(validated_data)
