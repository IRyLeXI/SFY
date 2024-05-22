from django.urls import path
from django.conf import settings
from author.views import *

urlpatterns = [
    path('get/all/', AuthorViewSet.as_view({'get': 'list'})),
    path('get/<int:pk>/', AuthorViewSet.as_view({'get': 'retrieve'})),
    path('create/', AuthorViewSet.as_view({'post': 'create'})),
    path('update/<int:pk>/',  AuthorViewSet.as_view({'put': 'update'})),
    path('patch/<int:pk>/',  AuthorViewSet.as_view({'patch': 'partial_update'})),
    path('delete/<int:pk>/', AuthorViewSet.as_view({'delete': 'destroy'})),
    path('<int:pk>/songs/', AuthorViewSet.as_view({'get': 'get_songs'})),
    path('<int:pk>/albums/', AuthorViewSet.as_view({'get': 'get_albums'})),
    path('created_songs/', AuthorViewSet.as_view({'get': 'get_created_songs'})),
]