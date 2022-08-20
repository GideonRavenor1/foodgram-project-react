from django.contrib import admin
from django.contrib.admin import display
from django.db.models import QuerySet
from django.http import HttpRequest

from .models.basic import Ingredient, Recipe, Tag
from .models.m2m import IngredientAmount, Favorite, ShoppingCart

EMPTY_VALUE = '-пусто-'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    empty_value_display = '-пусто-'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    list_filter = ('name',)
    search_fields = ('name',)
    empty_value_display = EMPTY_VALUE


class IngredientsInlineAdmin(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 0


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'author',
        'name',
        'image',
        'text',
        'subscribers',
        'all_ingredients',
    )
    fields = ()
    search_fields = ('author', 'name')
    list_filter = ('author', 'name', 'tags')
    inlines = (IngredientsInlineAdmin,)
    list_display_links = ('author',)
    empty_value_display = EMPTY_VALUE

    def subscribers(self, obj: Recipe) -> int:
        return Favorite.objects.filter(recipe=obj).count()

    @display(description='Ингредиенты')
    def all_ingredients(self, obj: Recipe) -> str:
        return ', '.join(obj.ingredients.values_list('name', flat=True))

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return (
            super()
            .get_queryset(request)
            .select_related('author')
            .prefetch_related('ingredients')
        )


@admin.register(IngredientAmount)
class IngredientAmountAdmin(admin.ModelAdmin):
    list_display = ('id', 'ingredient', 'recipe', 'amount')
    empty_value_display = EMPTY_VALUE


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    empty_value_display = EMPTY_VALUE


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    empty_value_display = EMPTY_VALUE
