from datetime import timedelta
from rest_framework import status, viewsets
from rest_framework.response import Response
from .models import Song
from .serializers import SongSerializer
from SFY.firebase_utils import upload_song_audio_firebase, upload_song_picture_firebase
from mutagen.mp3 import MP3

class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer

    def create(self, request, *args, **kwargs):
        audio_file = request.FILES.get('audio')
        picture_file = request.FILES.get('picture')

        if audio_file:
            audio_url = upload_song_audio_firebase(audio_file)
            request.data['audio_url'] = audio_url

            try:
                audio_info = MP3(audio_file)
                duration_in_seconds = int(audio_info.info.length)
                duration_formatted = str(timedelta(seconds=duration_in_seconds))
                request.data['duration'] = duration_formatted
            except Exception as e:
                print(f"Error extracting duration from MP3 file: {e}")

        if picture_file:
            picture_url = upload_song_picture_firebase(picture_file)
            request.data['picture_url'] = picture_url

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        audio_file = request.FILES.get('audio')
        picture_file = request.FILES.get('picture')

        if audio_file:
            audio_url = upload_song_audio_firebase(audio_file)
            request.data['audio_url'] = audio_url

        if picture_file:
            picture_url = upload_song_picture_firebase(picture_file)
            request.data['picture_url'] = picture_url

        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        audio_file = request.FILES.get('audio')
        picture_file = request.FILES.get('picture')

        if audio_file:
            audio_url = upload_song_audio_firebase(audio_file)
            request.data['audio_url'] = audio_url

        if picture_file:
            picture_url = upload_song_picture_firebase(picture_file)
            request.data['picture_url'] = picture_url

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
