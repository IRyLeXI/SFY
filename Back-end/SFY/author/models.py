from django.db import models
from user.models import CustomUser
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Author(CustomUser):
    description = models.CharField(_("author description"), max_length=2000, blank=True)
    
    header_picture = models.ImageField(_("header picture"), blank=True, null=True)
    
    is_author = models.BooleanField(_("is user author"), blank=True, null=True, default=True)
    
    
    