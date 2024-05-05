from django.shortcuts import render
from .models import Author
from rest_framework.response import Response
from rest_framework import status, generics, viewsets
from .serializers import AuthorSerializer

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer