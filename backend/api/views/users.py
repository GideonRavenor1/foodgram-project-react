from django.contrib.auth import get_user_model
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from ..serializers.users import CustomUserSerializer


User = get_user_model()


class CustomUserViewSet(DjoserUserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    swagger_tags = ('Users',)
