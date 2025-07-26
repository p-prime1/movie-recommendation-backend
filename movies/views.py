from django.shortcuts import render
from .model import Movie, Genre, Rating, UserProfile, Review
from .serializers import MovieSerializer, GenreSerializer, RatingSerializer, UserProfileSerializer, ReviewSerializer
from rest_framework import viewsets
# Create your views here.


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Moview.objects.all()
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


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer