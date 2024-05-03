from django.urls import path
from . import views
from django.conf import settings
from user.views import *

urlpatterns = [
    path('get/all/', UserViewSet.as_view({'get': 'list'})),
    path('update/<int:pk>/',  UserViewSet.as_view({'put': 'update'})),
    path('get/<int:pk>/', UserViewSet.as_view({'get': 'retrieve'})),
]