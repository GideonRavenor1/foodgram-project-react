from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.models import Follow
from .recipes import ShortRecipeSerializer


User = get_user_model()


class FollowSerializer(serializers.ModelSerializer):
    """
    Сериализатор для вывода подписок пользователя
    """

    is_subscribed = serializers.SerializerMethodField(read_only=True)
    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)

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

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes = obj.recipes.all()
        recipes_limit = request.query_params.get('recipes_limit')
        if recipes_limit:
            recipes = recipes[: int(recipes_limit)]
        return ShortRecipeSerializer(recipes, many=True).data

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Follow.objects.filter(user=user, author=obj.id).exists()

    def get_recipes_count(self, obj):
        return obj.recipes.count()
