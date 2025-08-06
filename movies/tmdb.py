import requests
from django.conf import settings

BASE_URL = 'https://api.themoviedb.org/3'


def search_movies(query):
    """Function searches for a movie in tmdb and returns the results"""
    url = f"{BASE_URL}/search/movie"

    params = {
        'api_key': settings.TMDB_API_KEY,
        'query': query,
    }

    response = requests.get(url, params)
    return response.json()