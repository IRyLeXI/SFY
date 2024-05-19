from django.shortcuts import render
from .models import Genre
from rest_framework.response import Response
from rest_framework import status, generics, viewsets, permissions
from .serializers import GenreSerializer
from rest_framework.views import APIView

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    
    
class SearchGenre(APIView):
    permission_classes=[permissions.IsAuthenticated]
    
    def get(self, request):
        query = request.query_params.get('query', None)
        if query is None:
            genres = Genre.objects.all()
        else:
            genres = Genre.objects.filter(name__istartswith=query)
        serializer = GenreSerializer(genres, many=True)
        return Response(serializer.data)