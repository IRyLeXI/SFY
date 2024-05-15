from django.utils import timezone
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework_simplejwt.models import TokenUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password

class CustomUserManager(BaseUserManager):
    use_in_migrations = True
    
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not username:
            raise ValueError('This username is not valid')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, username, password, **extra_fields)


class CustomUser(AbstractUser):
    
    username_validator = UnicodeUsernameValidator()
     
    username = models.CharField(
        _("username"),
        max_length=50,
        unique=True,
        help_text=_(
            "Required. 50 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    
    email = models.EmailField(_('email'), max_length=80, unique=True)
    
    birth_date = models.DateField(_("birthday date"), blank=True, null=True)
     
    picture_url = models.CharField(max_length=255, blank=True, null=True, default="sfy-firebase.appspot.com/profile_pictures/defaultuser.png")
    
    followers = models.ManyToManyField('CustomUser', through='UserFollowers', blank=True, null=True)
    
    is_author = models.BooleanField(_("is user author"), blank=True, null=True, default=False)
    
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ['email', 'first_name','last_name']
    
    objects = CustomUserManager()
    
    def __str__(self):
        return f"{self.username}"
    
    def save(self, *args, **kwargs):
        if self.password:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)


class UserFollowers(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='following')
    follower = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='follower')

    class Meta:
        db_table = 'user_followers'
               