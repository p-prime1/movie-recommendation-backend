from rest_framework import serializers
from .models import Genre, Rating, UserProfile, Movie
from django.contrib.auth.models import User

class GenreSerializer(serializers.ModelSerializer):
    """ Serializer for Genre model."""
    class Meta:
        model = Genre
        fields = '__all__'


class MovieSerializer(serializers.ModelSerializer):
    """ Serializer for Movie model."""
    genres = GenreSerializer(many=True, read_only=True)
    
    class Meta:
        model = Movie
        fields = '__all__'
        read_only_fields = ['average_rating']


class RatingSerializer(serializers.ModelSerializer):
    """ Serializer for movie ratings."""
    class Meta:
        model = Rating
        fields = '__all__'
        read_only_fields = ['timestamp']

class UserProfileSerializer(serializers.ModelSerializer):
    preferred_genres = GenreSerializer(many=True, read_only=True)
    class Meta:
        model = UserProfile
        fields = ['user', 'bio', 'birth_date', 'profile_picture', 'preferred_genres']


class UserSerializer(serializers.ModelSerializer):
    """ Serializer for User model to handle user creation."""
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', '')
        )
        return user



