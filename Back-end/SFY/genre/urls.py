from django.urls import path
from django.conf import settings
from genre.views import *

urlpatterns = [
    path('get/all/', GenreViewSet.as_view({'get': 'list'})),
    path('get/<int:pk>/', GenreViewSet.as_view({'get': 'retrieve'})),
    path('create/', GenreViewSet.as_view({'post': 'create'})),
    path('update/<int:pk>/',  GenreViewSet.as_view({'put': 'update'})),
    path('patch/<int:pk>/',  GenreViewSet.as_view({'patch': 'partial_update'})),
    path('delete/<int:pk>/', GenreViewSet.as_view({'delete': 'destroy'})),
    path('search/', SearchGenre.as_view()),
]