from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers
from djoser.serializers import UserSerializer as DjoserUserSerializer

from users.models import Follow

User = get_user_model()


class CustomUserSerializer(DjoserUserSerializer):
    is_subscribed = serializers.SerializerMethodField()

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
        read_only_fields = ('is_subscribed',)

    @swagger_serializer_method(serializer_or_field=serializers.BooleanField)
    def get_is_subscribed(self, obj: User) -> bool:
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return Follow.objects.filter(user=user, following=obj.id).exists()
