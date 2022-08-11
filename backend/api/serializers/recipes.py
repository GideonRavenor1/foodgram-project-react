from django.db import transaction
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField

from recipes.models.basic_models import Recipe, Tag
from recipes.models.m2m_models import Favorite, ShoppingCart, IngredientAmount
from ..serializers.users import CustomUserSerializer
from .ingredients import (
    IngredientAmountSerializer,
    CreateIngredientAmountSerializer,
)
from .tags import TagSerializer


class ShortRecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор краткого отображения сведений о рецепте
    """

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class RecipeListSerializer(serializers.ModelSerializer):
    """
    Сериализатор отображения рецептов
    """

    tags = TagSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField(read_only=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = '__all__'

    def get_ingredients(self, obj):
        queryset = IngredientAmount.objects.filter(recipe=obj)
        return IngredientAmountSerializer(queryset, many=True).data

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return Favorite.objects.filter(user=user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(user=user, recipe=obj).exists()


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField(use_url=True, max_length=None)
    author = CustomUserSerializer(read_only=True)
    ingredients = CreateIngredientAmountSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )
    cooking_time = serializers.IntegerField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'image',
            'tags',
            'author',
            'ingredients',
            'name',
            'text',
            'cooking_time',
        )

    def bulk_create(self, recipe, ingredients_data):
        elements = [
            IngredientAmount(
                ingredient=ingredient['ingredient'],
                recipe=recipe,
                amount=ingredient['amount'],
            )
            for ingredient in ingredients_data
        ]
        IngredientAmount.objects.bulk_create(elements)

    @transaction.atomic
    def create(self, validated_data):
        request = self.context['request']
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        recipe = Recipe.objects.create(author=request.user, **validated_data)
        recipe.tags.set(tags_data)
        self.bulk_create(recipe, ingredients_data)
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        IngredientAmount.objects.filter(recipe=instance).delete()
        self.bulk_create(instance, ingredients_data)
        instance.name = validated_data.pop('name')
        instance.text = validated_data.pop('text')
        instance.cooking_time = validated_data.pop('cooking_time')
        if validated_data.get('image') is not None:
            instance.image = validated_data.pop('image')

        instance.save()
        instance.tags.set(tags_data)
        return instance

    def validate_cooking_time(self, value):
        if int(value) <= 0:
            raise serializers.ValidationError(
                'Время приготовления должно быть больше 0.'
            )
        return value

    def to_representation(self, instance):
        context = {'request': self.context['request']}
        return RecipeListSerializer(instance, context=context).data
