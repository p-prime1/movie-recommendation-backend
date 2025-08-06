# Django
from django.shortcuts import render
from django.contrib.auth.models import User
from django.core.cache import cache
from django.db.models import Avg

# DRF
from rest_framework import viewsets, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import ValidationError

# Swagger
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Local
from .models import Movie, Genre, Rating, UserProfile
from .serializers import (
    MovieSerializer, GenreSerializer, RatingSerializer,
    UserProfileSerializer, UserSerializer
)
from .tmdb import search_movies

# Create your views here.



class SignupView(generics.CreateAPIView):
    """Signup view for creating new users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


    def perform_create(self, serializer):
        """Creates a user profile when a new user signs up"""
        return serializer.save()


        
class MovieViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    """ViewSet for movies.
    """
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    def list(self, request, *args, **kwargs):
        """List all movies available in the database."""
        # Check if the data is cached
        cache_key = 'all_movies'
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        cache.set(cache_key, data, timeout=60*5)

        return Response(data)


class GenreViewSet(viewsets.ModelViewSet):
    """ViewSet for genres.
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class RatingViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def perform_create(self, serializer):
        movie = serializer.validated_data.get('movie')
        user = self.request.user
        # Check if the user has already rated this movie
        existing_rating = Rating.objects.filter(user=user, movie=movie).first()
        if existing_rating:
            raise ValidationError("You have already rated this movie.")

        serializer.save(user=user)
    def get_queryset(self):
        """Filter ratings by the authenticated user."""
        user = self.request.user
        return Rating.objects.filter(user=user).order_by('-timestamp')
    


class UserProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for user profiles.
    """
    permission_classes = [IsAuthenticated]
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    def get_queryset(self):
        """Filter user profiles by the authenticated user."""
        user = self.request.user
        return UserProfile.objects.filter(user=user)

    def perform_update(self, serializer):
        """Update the user profile."""
        user = self.request.user
        serializer.save(user=user)


class TMDBSearchView(APIView):
    """Search for movies using TMDB API.
    """
    def get(self, request):
        query = request.query_params.get('q')

        if not query:
            return Response({'error': 'Query param `q` is required.'}, status=400)
        
        data = search_movies(query)
        return Response(data)


    def post(self, request):
        """Saves a new movie entry to the database."""
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
        )

        movie.genres.set(genres)
        movie.save()

        return Response({"message": "Movie saved succesfully!"}, status=status.HTTP_201_CREATED)


class RecommendationPagination(PageNumberPagination):
    """Custom pagination class for recommmendations"""
    page_size = 10
    ordering = '-created_at'



class RecommendationView(APIView):
    """View for getting movie recommendation based on user ratings."""
    permission_classes = [IsAuthenticated]

    def paginate_data(self, queryset, request):
        paginator = RecommendationPagination()
        page = paginator.paginate_queryset(queryset, request, view=self)
        if page is not None:
            serializer = MovieSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        serializer = MovieSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Get movie recommendations based on user's rated genres.",
        responses={200: MovieSerializer(many=True)}
    )
    def get(self, request):
        user = request.user
        ratings = Rating.objects.filter(user=user).order_by('-score')
        top_genres = {}

        for rating in ratings:
            for genre in rating.movie.genres.all():
                top_genres[genre.id] = top_genres.get(genre.id, 0) + rating.score

        paginator = RecommendationPagination()

        # Returns popular movies if the user has no ratings or genres
        if not top_genres:
            popular_movies = Movie.objects.annotate(
                avg_rating=Avg('ratings__score')
            ).order_by('-avg_rating').distinct()
            return self.paginate_data(popular_movies, request)

        sorted_genres = sorted(top_genres.items(), key=lambda x: x[1], reverse=True)
        top_genre_ids = [g[0] for g in sorted_genres[:3]]
        rated_movie_ids = ratings.values_list('movie_id', flat=True)

        recommended_movies = Movie.objects.filter(
            genres__in=top_genre_ids
        ).exclude(id__in=rated_movie_ids).order_by('-created_at').distinct()

        return self.paginate_data(recommended_movies, request)