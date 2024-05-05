from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from author.models import Author
from playlist.models import Playlist
import datetime

class Song(models.Model):
    name = models.CharField(_("song name"), max_length=200, blank=False, null=False, unique=False)
    
    duration = models.DurationField(_("duration"), blank=True, null=True)
    
    listened_num = models.IntegerField(_("number of listens"), default=0, blank=True, null=True)
    
    publication_date = models.DateTimeField(_("publication date"), blank = True, null=True, default=timezone.now())
    
    picture = models.ImageField(_("picture"), blank=True, null=True)
    
    authors = models.ManyToManyField(Author, blank=False, through='SongAuthors', related_name="songs")
    
    playlists = models.ManyToManyField(Playlist, blank=True, null=True, through='PlaylistSongs', related_name="songs")

    def __str__(self):
        return self.name


class SongAuthors(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    class Meta:
        db_table = 'song_authors'
        

class PlaylistSongs(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)

    class Meta:
        db_table = 'playlist_songs'