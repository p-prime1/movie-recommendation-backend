from django.shortcuts import render
from .models import Movie, Genre, Rating, UserProfile
from .serializers import MovieSerializer, GenreSerializer, RatingSerializer, UserProfileSerializer
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response 
from .tmdb import search_movies
# Create your views here.


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class TMDBSearchView(APIView):
    def get(self, request):
        query = request.query_params.get('q')

        if not query:
            return Response({'error': 'Query param `q` is required.'}, status=400)
        
        data = search_movies(query)
        return Response(data)


    def post(self, request):
        data = request.data

        genres = []
        for genre_name in data.get('genres', []):
            genre, _ = Genre.objects.get_or_create(name=genre_name)
            genres.append(genre)

        movie = Movie.objects.create(
            title = data.get("title"),
            description = data.get("description"),
            release_date = data.get("release_date"),
            duration = data.get("duration", 0),
            rating = data.get("rating"),
            overview = data.get("overview"),
        )

        movie.genres.set(genres)
        movies.save()

        return Response({"message": "Movie saved succesfully!"}, status=status.HTTP_201_CREATED)