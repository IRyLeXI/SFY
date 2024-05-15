from django.db import models
from user.models import CustomUser
from django.utils.translation import gettext_lazy as _

class Author(CustomUser):
    description = models.CharField(_("author description"), max_length=2000, blank=True)
    
    header_picture = models.ImageField(_("header picture"), blank=True, null=True)
    
    def save(self, *args, **kwargs):
        self.is_author = True
        super().save(*args, **kwargs)
    
    
    