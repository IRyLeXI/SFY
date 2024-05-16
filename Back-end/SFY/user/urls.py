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
    path('upload_picture/', UploadPictureView.as_view(), name='upload_picture'),
    path('follow/<int:pk>/', UserViewSet.as_view({'post': 'follow'})),
    path('unfollow/<int:pk>/', UserViewSet.as_view({'delete': 'unfollow'})),
]