from django.db import models
import datetime
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from user.models import CustomUser
from author.models import Author
from song.models import Song
from genre.models import Genre
from playlist.mixins import GenreSetMixin

class Album(models.Model, GenreSetMixin):
    title = models.CharField(_("album title"), max_length=60, null=False, blank=False, help_text="Title cannot be empty", unique=False)
    
    picture_url = models.CharField(_("album picture"), max_length=255, blank=True, null=True, default="sfy-firebase.appspot.com/albums_pictures/defaultalbum.png")
    
    created_date = models.DateTimeField(_("created date"), default=timezone.now, editable=False)
    
    publish_date = models.DateTimeField(_("publish date"), default=timezone.now, blank=True, null=True)
    
    owner = models.ForeignKey(Author, on_delete=models.CASCADE, blank=False, related_name="albums")
    
    major_genre = models.ForeignKey(Genre, on_delete=models.CASCADE, blank=True, null=True, related_name="albums")
    
    songs = models.ManyToManyField(Song, blank=True, null=True, through='AlbumsSongs', related_name="albums")
    
    followers = models.ManyToManyField(CustomUser, blank=True, null=True, related_name="followed_albums")
    
    def __str__(self):
        return self.title


        
class AlbumsSongs(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)

    class Meta:
        db_table = 'albums_songs'
                