from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from user.models import CustomUser
from django.utils.translation import gettext_lazy as _

class Author(CustomUser):
    description = models.CharField(_("author description"), max_length=2000, blank=True)
    
    header_picture = models.ImageField(_("header picture"), blank=True, null=True)
    
    def save(self, *args, **kwargs):
        self.is_author = True
        super().save(*args, **kwargs)
        
        
        
               
@receiver(post_save, sender=Author)
def create_default_playlists(sender, instance, created, **kwargs):
    if created:
        from playlist.models import Playlist
        liked_songs_playlist = Playlist.objects.create(
            title="Liked songs",
            owner=instance,
            picture_url = 'sfy-firebase.appspot.com/playlists_pictures/liked_songs_playlist.png',
            is_private=True,
            is_generated=True
        )
        liked_songs_playlist.followers.add(instance)
        liked_songs_playlist.save()

        daily_recommendations_playlist = Playlist.objects.create(
            title="Daily Recommendations",
            owner=instance,
            picture_url = 'sfy-firebase.appspot.com/playlists_pictures/daily_playlist.jpg',
            is_private=True,
            is_generated=True
        )
        daily_recommendations_playlist.followers.add(instance)
        daily_recommendations_playlist.save()           