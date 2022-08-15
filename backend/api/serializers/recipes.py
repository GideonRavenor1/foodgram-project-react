from django.db import transaction
from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField

from recipes.models.basic import Recipe, Tag
from recipes.models.m2m import Favorite, ShoppingCart, IngredientAmount
from ..serializers.users import CustomUserSerializer
from .ingredients import (
    IngredientAmountSerializer,
    CreateIngredientAmountSerializer,
)
from .tags import TagSerializer


class ShortRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class RecipeListSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    author = CustomUserSerializer()
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
    image = Base64ImageField(use_url=True, max_length=None)
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

    def bulk_create(self, recipe, ingredients_data):
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
