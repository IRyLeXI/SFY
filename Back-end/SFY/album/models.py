from django.db import models
import datetime
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from user.models import CustomUser
from author.models import Author

class Album(models.Model):
    title = models.CharField(_("album title"), max_length=60, null=False, blank=False, help_text="Title cannot be empty", unique=False)
    
    picture_url = models.CharField(_("album picture"), max_length=255, blank=True, null=True, default="sfy-firebase.appspot.com/albums_pictures/defaultalbum.png")
    
    created_date = models.DateField(_("created date"), blank=False, default=timezone.now().date(), editable=False)
    
    publish_date = models.DateField(_("publish date"), blank=True, default=timezone.now().date(), editable=True)
    
    owner = models.ForeignKey(Author, on_delete=models.CASCADE, blank=False, related_name="albums")
    
    followers = models.ManyToManyField(CustomUser, blank=True, null=True, related_name="followed_albums")
    
    def __str__(self):
        return self.title


