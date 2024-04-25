from django.urls import path
from . import views
from django.conf import settings

urlpatterns = [
    path('all/', views.getData),
    path('post/', views.postData),
]