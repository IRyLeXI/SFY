from django.urls import path
from . import views
from django.conf import settings
from user.views import *

urlpatterns = [
    path('update/<int:pk>/', UserAPIUpdate.as_view()),
    path('detail/<int:pk>/', UserAPIDetailView.as_view()),
]