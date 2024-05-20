from django.urls import path
from django.conf import settings
from user.views import *

urlpatterns = [
    path('get/all/', UserViewSet.as_view({'get': 'list'})),
    path('get/<int:pk>/', UserViewSet.as_view({'get': 'retrieve'})),
    path('create/', UserViewSet.as_view({'post': 'create'})),
    path('update/<int:pk>/',  UserViewSet.as_view({'put': 'update'})),
    path('patch/<int:pk>/',  UserViewSet.as_view({'patch': 'partial_update'})),
    path('delete/<int:pk>/', UserViewSet.as_view({'delete': 'destroy'})),
    path('get/<int:pk>/playlists/', UserViewSet.as_view({'get': 'get_user_playlists'})),
    path('get/<int:pk>/followed/', UserViewSet.as_view({'get': 'get_user_followed_to'})),
    path('get/followed/music/', UserViewSet.as_view({'get': 'get_user_followed_albums_playlists'})),
    path('check/', UserViewSet.as_view({'get': 'is_logged_in'})),
    path('upload_picture/', UploadPictureView.as_view(), name='upload_picture'),
    path('follow/<int:pk>/', UserViewSet.as_view({'post': 'follow'})),
    path('unfollow/<int:pk>/', UserViewSet.as_view({'delete': 'unfollow'})),
    path('genre/favourite/', UserRecommendations.as_view({'get': 'get_user_favorite_genre'})),
    path('song_listen/listen/', UserListen.as_view({'post': 'listen'})),
    path('song_listen/<int:pk>/', UserListen.as_view({'get': 'get_by_song'})),
    path('song_listen/<int:pk>', UserListen.as_view({'patch': 'patch_song_listen'})),
    path('song_listen/stop/', UserListen.as_view({'patch': 'stop_last_listen'})),
    path('search/', UserRecommendations.as_view({'get': 'search'})),
]