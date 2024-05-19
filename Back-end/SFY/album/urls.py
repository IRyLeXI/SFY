from django.urls import path
from django.conf import settings
from album.views import *

urlpatterns = [
    path('get/all/', AlbumViewSet.as_view({'get': 'list'})),
    path('get/<int:pk>/', AlbumViewSet.as_view({'get': 'retrieve'})),
    path('create/', AlbumViewSet.as_view({'post': 'create'})),
    path('update/<int:pk>/',  AlbumViewSet.as_view({'put': 'update'})),
    path('patch/<int:pk>/',  AlbumViewSet.as_view({'patch': 'partial_update'})),
    path('delete/<int:pk>/', AlbumViewSet.as_view({'delete': 'destroy'})),
    path('upload_picture/<int:pk>/', UploadPictureView.as_view(), name='upload_album_picture'),
    path('<int:pk>/songs/', AlbumViewSet.as_view({'get': 'get_songs'})),
    path('<int:pk>/add_song/', AlbumViewSet.as_view({'post': 'add_song'})),
    path('<int:pk>/add_songs/', AlbumViewSet.as_view({'post': 'add_songs'})),
    path('<int:pk>/follow/', AlbumViewSet.as_view({'post': 'follow'})),
    path('<int:pk>/unfollow/', AlbumViewSet.as_view({'delete': 'unfollow'})),
    path('recommended/', AlbumViewSet.as_view({'get': 'get_recommended_albums'})),
]