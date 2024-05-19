from django.urls import path
from django.conf import settings
from song.views import *

urlpatterns = [
    path('get/all/', SongViewSet.as_view({'get': 'list'})),
    path('get/<int:pk>/', SongViewSet.as_view({'get': 'retrieve'})),
    path('create/', SongViewSet.as_view({'post': 'create'})),
    path('update/<int:pk>/',  SongViewSet.as_view({'put': 'update'})),
    path('patch/<int:pk>/',  SongViewSet.as_view({'patch': 'partial_update'})),
    path('delete/<int:pk>/', SongViewSet.as_view({'delete': 'destroy'})),
    path('genres/<int:pk>/', SongViewSet.as_view({'patch': 'update_genres'})),
]