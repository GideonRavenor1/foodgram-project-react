from rest_framework import serializers

from recipes.models.m2m_models import ShoppingCart
from ..serializers.recipes import ShortRecipeSerializer


class ShoppingCartSerializer(serializers.ModelSerializer):
    """
    Сериализатор списка покупок
    """

    class Meta:
        model = ShoppingCart
        fields = ('user', 'recipe')

    def to_representation(self, instance):
        context = {'request': self.context['request']}
        return ShortRecipeSerializer(instance.recipe, context=context).data
