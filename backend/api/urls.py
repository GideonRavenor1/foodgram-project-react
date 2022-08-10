from django.urls import include, path

from .swagger.urls import urlpatterns as swagger_urls

app_name = 'api'

urlpatterns = [
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]

urlpatterns += swagger_urls
