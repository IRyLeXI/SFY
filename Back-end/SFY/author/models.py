from datetime import timedelta
from django.utils import timezone
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
        if not self.picture_url:
            self.picture_url = "https://storage.googleapis.com/sfy-firebase.appspot.com/profile_pictures/defaultuser.png"
        super().save(*args, **kwargs)
        
        
        
               
@receiver(post_save, sender=Author)
def create_default_playlists(sender, instance, created, **kwargs):
    if created:
        from playlist.models import Playlist
        liked_songs_playlist = Playlist.objects.create(
            title="Liked songs",
            owner=instance,
            picture_url = 'https://storage.googleapis.com/sfy-firebase.appspot.com/playlists_pictures/liked_songs_playlist.png',
            is_private=True,
            is_generated=False
        )
        liked_songs_playlist.followers.add(instance)
        liked_songs_playlist.save()

        helper_playlist = Playlist.objects.create(
            title="Helper playlist",
            owner=instance,
            picture_url = 'https://storage.googleapis.com/sfy-firebase.appspot.com/playlists_pictures/defaultplaylist.png',
            is_private=True,
            is_generated=True
        )
        helper_playlist.followers.add(instance)
        helper_playlist.save()

        for i in range(1,4):
            daily_recommendations_playlist = Playlist.objects.create(
                title=f"Daily Recommendations {i}",
                owner=instance,
                picture_url = f'https://storage.googleapis.com/sfy-firebase.appspot.com/playlists_pictures/daily_recommendations{i}.jpg',
                is_private=True,
                is_generated=True,
                updated_date = timezone.now() - timedelta(days=1, hours=1)      
            )
            daily_recommendations_playlist.followers.add(instance)
            daily_recommendations_playlist.save() 