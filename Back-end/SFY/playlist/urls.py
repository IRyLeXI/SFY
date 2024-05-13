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
]