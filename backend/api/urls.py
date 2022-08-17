from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .swagger.urls import urlpatterns as swagger_urls
from .views.Ingredients import IngredientsViewSet
from .views.follows import FollowAPIView, FollowListAPIView
from .views.recipe import RecipeViewSet
from .views.tags import TagsViewSet
from .views.users import CustomUserViewSet

app_name = 'api'

router = DefaultRouter()
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('ingredients', IngredientsViewSet, basename='ingredients')
router.register('tags', TagsViewSet, basename='tags')
router.register('users', CustomUserViewSet, basename='users')

urlpatterns = [
    path(
        'users/subscriptions/',
        FollowListAPIView.as_view(),
        name='subscriptions',
    ),
    path(
        'users/<int:user_id>/subscribe/',
        FollowAPIView.as_view(),
        name='subscribe',
    ),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]

urlpatterns += swagger_urls
