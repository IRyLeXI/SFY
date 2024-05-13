from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Genre(models.Model):
    name = models.CharField(_("author description"), max_length=200, blank=False, null=False)