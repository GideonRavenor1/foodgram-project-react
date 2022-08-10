from django.urls import path, re_path

from drf_yasg import openapi

from drf_yasg.views import get_schema_view

from rest_framework import permissions

# Схема и ссылки сваггера.


schema_view = get_schema_view(
    openapi.Info(
        title='FoodGram-API',
        default_version='v1',
        description='API дипломного проекта FoodGram-API',
        contact=openapi.Contact(email='Gideon-Ravenor1@yandex.ru'),
        license=openapi.License(name='BSD License'),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    re_path(
        r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json',
    ),
    path(
        'swagger/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui',
    ),
    path(
        'redoc/',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc',
    ),
]
