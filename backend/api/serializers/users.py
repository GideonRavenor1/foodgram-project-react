from django.contrib.auth import get_user_model
from rest_framework import serializers
from djoser.serializers import UserSerializer as DjoserUserSerializer

from users.models import Follow

User = get_user_model()


class CustomUserSerializer(DjoserUserSerializer):
    """
    Сериализатор пользователя.
    """

    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return Follow.objects.filter(user=user, author=obj.id).exists()
