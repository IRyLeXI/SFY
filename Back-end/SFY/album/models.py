from django.db import models
import datetime
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from user.models import CustomUser
from author.models import Author

# Create your models here.
class Album(models.Model):
    title = models.CharField(_("album title"), max_length=60, null=False, blank=False, help_text="Title cannot be empty", unique=False)
    
    picture = models.ImageField(_("album image"), blank=True, null=True)
    
    created_date = models.DateField(_("created date"), blank=False, default=timezone.now().date(), editable=False)
    
    owner = models.ForeignKey(Author, on_delete=models.CASCADE, blank=False, related_name="albums")
    
    followers = models.ManyToManyField(CustomUser, blank=True, null=True, related_name="followed_albums")
    
    def __str__(self):
        return self.title


