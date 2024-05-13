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
]