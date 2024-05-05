from django.db import models
import datetime
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from user.models import CustomUser

# Create your models here.
class Playlist(models.Model):
    title = models.CharField(_("playlist title"), max_length=60, null=False, blank=False, help_text="Title cannot be empty", unique=False)
    
    picture = models.ImageField(_("playlist image"), blank=True, null=True)
    
    created_date = models.DateField(_("created date"), blank=False, default=timezone.now().date(), editable=False)
    
    updated_date = models.DateField(_("updated date"), blank=False, default=timezone.now().date())
    
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=False, related_name="playlists")
    
    is_private = models.BooleanField(_("is private"), blank = True, null=True, default=True)
    
    followers = models.ManyToManyField(CustomUser, blank=True, null=True, related_name="followed_playlists",)
    
    def __str__(self):
        return self.title
    