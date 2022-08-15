from django.contrib.auth import get_user_model
from rest_framework import serializers
from drf_yasg.utils import swagger_serializer_method

from users.models import Follow
from .recipes import ShortRecipeSerializer


User = get_user_model()


class FollowSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )
        read_only_fields = ('is_subscribed', 'recipes', 'recipes_count')

    @swagger_serializer_method(
        serializer_or_field=ShortRecipeSerializer(many=True)
    )
    def get_recipes(self, obj: User) -> dict:
        request = self.context.get('request')
        recipes = obj.recipes.all()
        recipes_limit = request.query_params.get('recipes_limit')
        if recipes_limit:
            recipes = recipes[: int(recipes_limit)]
        return ShortRecipeSerializer(recipes, many=True).data

    @swagger_serializer_method(serializer_or_field=serializers.BooleanField)
    def get_is_subscribed(self, obj: User) -> bool:
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Follow.objects.filter(user=user, following=obj).exists()

    @swagger_serializer_method(serializer_or_field=serializers.IntegerField)
    def get_recipes_count(self, obj: User) -> int:
        return obj.recipes.count()
