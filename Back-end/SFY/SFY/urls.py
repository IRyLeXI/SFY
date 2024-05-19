"""
URL configuration for SFY project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from user.views import *
from playlist.views import *
from author.views import *
from song.views import *
from genre.views import *
from album.views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

# router = routers.SimpleRouter()

# router.register(r'user', UserViewSet)
# router.register(r'playlist', PlaylistViewSet)
# router.register(r'author', AuthorViewSet)
# router.register(r'song', SongViewSet)


urlpatterns = [
    # path('admin/', admin.site.urls),
    path('api/user/', include('user.urls')),
    path('api/playlist/', include('playlist.urls')),
    path('api/author/', include('author.urls')),
    path('api/song/', include('song.urls')),
    path('api/genre/', include('genre.urls')),
    path('api/album/', include('album.urls')),
    # path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify', TokenVerifyView.as_view(), name='token_verify'),
]
