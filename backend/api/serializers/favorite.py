from rest_framework import serializers

from api.serializers.recipes import ShortRecipeSerializer
from recipes.models.m2m_models import Favorite


class FavoriteSerializer(serializers.ModelSerializer):
    """
    Сериализатор списка избранного
    """

    class Meta:
        model = Favorite
        fields = ('user', 'recipe')

    def validate(self, data):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        recipe = data['recipe']
        if Favorite.objects.filter(user=request.user, recipe=recipe).exists():
            raise serializers.ValidationError(
                {'status': 'Рецепт уже добавлен в избранное.'}
            )
        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return ShortRecipeSerializer(instance.recipe, context=context).data
