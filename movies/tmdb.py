import requests
from django.conf import settings

BASE_URL = 'https://api.themoviedb.org/3'
TMDB_API_KEY = settings.TMDB_API_KEY


def search_movies(query):
    """Function searches for a movie in tmdb and returns the results"""
    url = f"{BASE_URL}/search/movie"

    params = {
        'api_key': settings.TMDB_API_KEY,
        'query': query,
    }

    response = requests.get(url, params)
    return response.json()


 
def get_popular_movies(page=1):
    url = f"{BASE_URL}/movie/popular"
    params = {
        "api_key": TMDB_API_KEY,
        "language": "en-US",
        "page": page
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()