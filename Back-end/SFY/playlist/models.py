from django.db import models
import datetime
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from user.models import CustomUser
from song.models import Song
from genre.models import Genre
from .mixins import GenreSetMixin

# Create your models here.
class Playlist(models.Model, GenreSetMixin):
    title = models.CharField(_("playlist title"), max_length=60, null=False, blank=False, help_text="Title cannot be empty", unique=False)
    
    picture_url = models.CharField(_("playlist picture"), max_length=255, blank=True, null=True, default="sfy-firebase.appspot.com/playlists_pictures/defaultplaylist.png")
    
    created_date = models.DateTimeField(_("created date"), default=timezone.now, editable=False)
    
    updated_date = models.DateTimeField(_("updated date"), default=timezone.now, blank=True, null=True)
    
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=False, related_name="playlists")
    
    major_genre = models.ForeignKey(Genre, on_delete=models.CASCADE, blank=True, null=True, related_name="playlists")
    
    is_private = models.BooleanField(_("is private"), blank = True, null=True, default=True)
    
    is_generated = models.BooleanField(_("is generated"), blank = True, null=True, default=False)
    
    songs = models.ManyToManyField(Song, blank=True, null=True, through='PlaylistsSongs', related_name="playlists")
    
    followers = models.ManyToManyField(CustomUser, blank=True, null=True, related_name="followed_playlists",)
    
    def __str__(self):
        return self.title
    
    
class PlaylistsSongs(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)

    class Meta:
        db_table = 'playlists_songs'    
        
        
       