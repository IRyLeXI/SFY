from django.urls import path
from django.conf import settings
from playlist.views import *

urlpatterns = [
    path('get/all/', PlaylistViewSet.as_view({'get': 'list'})),
    path('get/<int:pk>/', PlaylistViewSet.as_view({'get': 'retrieve'})),
    path('create/', PlaylistViewSet.as_view({'post': 'create'})),
    path('update/<int:pk>/',  PlaylistViewSet.as_view({'put': 'update'})),
    path('patch/<int:pk>/',  PlaylistViewSet.as_view({'patch': 'partial_update'})),
    path('delete/<int:pk>/', PlaylistViewSet.as_view({'delete': 'destroy'})),
    path('get/global/', PlaylistViewSet.as_view({'get': 'get_global_playlists'})),
    path('get/recommendations/', PlaylistViewSet.as_view({'get': 'get_daily_playlists'})),
    path('upload_picture/<int:pk>/', UploadPictureView.as_view(), name='upload_playlist_picture'),
    path('<int:pk>/songs/', PlaylistViewSet.as_view({'get': 'get_songs'})),
    path('<int:pk>/add_song/', PlaylistViewSet.as_view({'post': 'add_song'})),
    path('<int:pk>/follow/', PlaylistViewSet.as_view({'post': 'follow'})),
    path('<int:pk>/unfollow/', PlaylistViewSet.as_view({'delete': 'unfollow'})),
    path('daily/<int:pk>/', PlaylistGenerators.as_view({'get': 'get_daily_playlist'})),
    path('admin/update/', PlaylistGenerators.as_view({'post': 'update_admin_playlists'})),
    path('radio/', PlaylistGenerators.as_view({'post': 'generate_playlist_from_song'})),
]