from rest_framework.routers import DefaultRouter
from .views import MovieViewSet, GenreViewSet, UserProfileViewSet, RatingViewSet, TMDBSearchView, RecommendationView
from django.urls import path

router = DefaultRouter()
router.register(r'movies', MovieViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'users', UserProfileViewSet)
router.register(r'ratings', RatingViewSet)

urlpatterns = router.urls
urlpatterns += [
    path('tmdb/search/', TMDBSearchView.as_view(), name='tmdb-search'),
    path('recommendations/', RecommendationView.as_view(), name='recommendations'),
    path('signup/', SignupView.as_view(), name='signup'),
]