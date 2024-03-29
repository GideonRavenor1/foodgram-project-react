from django.db import transaction
from drf_extra_fields.fields import Base64ImageField
from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

from recipes.models.basic import Recipe, Tag
from recipes.models.m2m import Favorite, ShoppingCart, IngredientAmount
from .ingredients import (
    IngredientAmountSerializer,
    CreateIngredientAmountSerializer,
)
from .tags import TagSerializer
from ..serializers.users import CustomUserSerializer


class ShortRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class RecipeListSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    author = CustomUserSerializer()
    image = Base64ImageField()
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = '__all__'

    def get_fields(self) -> dict:
        fields = super().get_fields()
        for field in fields.values():
            field.read_only = True
        return fields

    @swagger_serializer_method(
        serializer_or_field=IngredientAmountSerializer(many=True)
    )
    def get_ingredients(self, obj: Recipe) -> dict:
        queryset = IngredientAmount.objects.filter(recipe=obj)
        return IngredientAmountSerializer(queryset, many=True).data

    @swagger_serializer_method(serializer_or_field=serializers.BooleanField)
    def get_is_favorited(self, obj: Recipe) -> bool:
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return Favorite.objects.filter(user=user, recipe=obj).exists()

    @swagger_serializer_method(serializer_or_field=serializers.BooleanField)
    def get_is_in_shopping_cart(self, obj: Recipe) -> bool:
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(user=user, recipe=obj).exists()


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
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
            'ingredients',
            'name',
            'text',
            'cooking_time',
        )
        read_only_fields = ('tags',)

    def bulk_create(self, recipe, ingredients_data) -> None:
        elements = [
            IngredientAmount(
                ingredient=ingredient['id'],
                recipe=recipe,
                amount=ingredient['amount'],
            )
            for ingredient in ingredients_data
        ]
        IngredientAmount.objects.bulk_create(elements)

    @transaction.atomic
    def create(self, validated_data) -> Recipe:
        request = self.context['request']
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        recipe = Recipe.objects.create(author=request.user, **validated_data)
        recipe.tags.set(tags_data)
        self.bulk_create(recipe, ingredients_data)
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data) -> Recipe:
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        IngredientAmount.objects.filter(recipe=instance).delete()
        self.bulk_create(instance, ingredients_data)
        instance.tags.set(tags_data)
        return super().update(instance, validated_data)

    def validate_cooking_time(self, value) -> int:
        if value <= 0:
            raise serializers.ValidationError(
                'Время приготовления должно быть больше 0.'
            )
        return value

    def to_representation(self, instance) -> dict:
        context = {'request': self.context['request']}
        return RecipeListSerializer(instance, context=context).data
