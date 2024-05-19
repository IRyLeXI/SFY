from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from author.models import Author
from genre.models import Genre
import datetime

class Song(models.Model):
    name = models.CharField(_("song name"), max_length=200, blank=False, null=False, unique=False)
    
    duration = models.DurationField(_("duration"), blank=True, null=True)
    
    listened_num = models.IntegerField(_("number of listens"), default=0, blank=True, null=True)
    
    publication_date = models.DateTimeField(_("publication date"), blank = True, null=True, default=timezone.now())
    
    audio_url = models.CharField(_("audio URL"), max_length=500, blank=False, null=False, default="https://storage.googleapis.com/sfy-firebase.appspot.com/songs/audio/nevergonnagiveyouup.mp3",)
    
    picture_url = models.CharField(_("picture URL"), max_length=500, blank=True, null=True, default="https://storage.googleapis.com/sfy-firebase.appspot.com/songs/pictures/note.png")
    
    authors = models.ManyToManyField(Author, blank=False, through='SongAuthors', related_name="songs")
    
    genres = models.ManyToManyField(Genre, through='SongGenres', related_name="songs")

    def __str__(self):
        return self.name


class SongAuthors(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    class Meta:
        db_table = 'songs_authors'
        
        
class SongGenres(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    priority = models.IntegerField(_("priority"))

    class Meta:
        db_table = 'songs_genres'        