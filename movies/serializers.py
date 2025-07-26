from rest_framework import serializers
from .models import Genre, Rating, UserProfile, Movie

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = '__all__'
        read_only_fields = ['average_rating']


class RatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rating
        fields = '__all__'
        read_only_fields = ['timestamp']

class UserProfileSerializer(serializers.ModelSerializer):
    preferred_genres = GenreSerializer(many=True, read_only=True)
    class Meta:
        model = UserProfile
        fields = ['user', 'bio', 'birth_date', 'profile_picture', 'preferred_genres']



