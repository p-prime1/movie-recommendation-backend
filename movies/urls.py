from rest_framework.routers import DefaultRouter
from .views import MovieViewSet, GenreViewSet, UserProfileViewSet, RatingViewSet, ReviewViewSet


router = DefaultRouter()
router.register(r'movies', MovieViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'users', UserProfileViewSet)
router.register(r'ratings', RatingViewSet)
router.register(r'reviews', ReviewViewSet)

urlpatterns = router.urls