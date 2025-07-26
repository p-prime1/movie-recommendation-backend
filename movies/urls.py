from rest_framework.routers import DefaultRouter
from .views import MovieViewSet, GenreViewSet, UserProfileViewSet, RatingViewSet


router = DefaultRouter()
router.register(r'movies', MovieViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'users', UserProfileViewSet)
router.register(r'ratings', RatingViewSet)

urlpatterns = router.urls