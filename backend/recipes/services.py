import math
import random
from urllib.parse import urljoin

import requests
from deep_translator import GoogleTranslator
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.db import IntegrityError
from django.db.models import QuerySet
from django.utils.html import strip_tags
from rest_framework.generics import get_object_or_404

from .models.basic import Recipe, Tag, Ingredient
from .models.m2m import IngredientAmount
from .type_annotations import RecipeResult, IngredientResult

User = get_user_model()


class RecipesCrawler:
    API_URL = settings.SPOONACULAR_API_URL
    API_KEY = settings.SPOONACULAR_API_KEY
    HEADERS = settings.SPOONACULAR_HEADERS

    def __init__(self, tag: str):
        self._data = None
        self._tag = tag

    def execute(self) -> None:
        response = requests.get(url=self._get_url(), headers=self.HEADERS)
        response.raise_for_status()
        self._data = response.json().get('recipes')

    @property
    def result(self) -> list[dict]:
        return self._data

    def _get_url(self) -> str:
        return urljoin(
            base=self.API_URL,
            url=self._prepare_query_params(),
        )

    def _prepare_query_params(self) -> str:
        number_of_recipes = self._get_number_of_recipes()
        return (
            f'recipes/random?number={number_of_recipes}'
            f'&tags={self._tag}'
            f'&apiKey={self.API_KEY}'
        )

    @staticmethod
    def _get_number_of_recipes() -> int:
        return random.randint(4, 8)


class JsonParser:
    DEFAULT_UNIT = 'шт'

    def __init__(self, data: list[dict], tag: str) -> None:
        self._data = data
        self._result = []
        self._tag = tag
        self._recipe = RecipeResult()
        self._ingredient = IngredientResult()
        self._recipe_fields = list(RecipeResult.__annotations__)
        self._ingredient_fields = list(IngredientResult.__annotations__)

    def parse(self) -> None:
        for recipe in self._data:
            for field in self._recipe_fields:
                getattr(self, f'_set_{field}')(
                    element=recipe, data=self._recipe
                )
            self._add_recipe_to_result()

    @property
    def result(self) -> list:
        return self._result

    def _set_name(
        self, element: dict, data: RecipeResult | IngredientResult
    ) -> None:
        data['name'] = self._translate_string(
            string=element.get('title') or element.get('name')
        )

    def _set_text(
        self, element: dict, data: RecipeResult | IngredientResult
    ) -> None:
        data['text'] = self._translate_string(string=element['summary'])

    def _set_image(
        self, element: dict, data: RecipeResult | IngredientResult
    ) -> None:
        data['image'] = element['image']

    def _set_cooking_time(
        self, element: dict, data: RecipeResult | IngredientResult
    ) -> None:
        data['cooking_time'] = element['readyInMinutes']

    def _set_tag(
        self, element: dict, data: RecipeResult | IngredientResult
    ) -> None:
        data['tag'] = self._tag

    def _set_ingredients(
        self, element: dict, data: RecipeResult | IngredientResult
    ) -> None:
        ingredients = element['extendedIngredients']
        data['ingredients'] = []
        for ingredient in ingredients:
            for field in self._ingredient_fields:
                getattr(self, f'_set_{field}')(
                    element=ingredient, data=self._ingredient
                )
            data['ingredients'].append(self._add_ingredient_to_recipe())

    def _set_amount(
        self, element: dict, data: RecipeResult | IngredientResult
    ) -> None:
        data['amount'] = math.ceil(element['measures']['us']['amount'])

    def _set_measurement_unit(
        self, element: dict, data: RecipeResult | IngredientResult
    ) -> None:
        unit = element['measures']['us']['unitLong'].lower()
        if unit:
            unit = self._translate_string(string=unit)
        else:
            unit = self.DEFAULT_UNIT
        data['measurement_unit'] = unit

    def _add_ingredient_to_recipe(self) -> IngredientResult:
        ingredients = self._ingredient.copy()
        self._ingredient.clear()
        return ingredients

    def _add_recipe_to_result(self) -> None:
        recipe = self._recipe.copy()
        self._recipe.clear()
        self._result.append(recipe)

    @staticmethod
    def _translate_string(
        string: str, source: str = 'en', target: str = 'ru'
    ) -> str:
        return GoogleTranslator(source=source, target=target).translate(
            strip_tags(string)
        )


class RecipeSaver:
    def __init__(self, data: list[dict]) -> None:
        self._data = data
        self._ingredient_names = None
        self._ingredient_units = None
        self._count = 0

    def save(self) -> int:
        user = self._get_superuser()
        for recipe in self._data:
            ingredients_data = recipe.pop('ingredients')

            try:
                recipe = self._save_recipe(user=user, data=recipe)
            except IntegrityError:
                continue

            self._bulk_create(recipe=recipe, data=ingredients_data)
            self._count += 1

        return self._count

    def _save_recipe(self, user: User, data: dict) -> Recipe:
        tag_data = data.pop('tag')
        url = data.pop('image')
        image, name = self._get_image(url=url)
        recipe = Recipe(author=user, **data)
        recipe.image.save(name, ContentFile(image))
        recipe.save()
        recipe.tags.set(self._get_tag(tag_data))
        return recipe

    @staticmethod
    def _get_superuser() -> QuerySet:
        return get_object_or_404(User, is_superuser=True)

    @staticmethod
    def _get_tag(tag) -> QuerySet:
        return Tag.objects.filter(slug=tag)

    @staticmethod
    def _get_image(url: str) -> tuple[bytes, str]:
        response = requests.get(url)
        response.raise_for_status()
        data = response.content
        filename = url.split('/')[-1]
        return data, filename

    def _bulk_create(self, recipe: Recipe, data: list[dict]) -> None:
        self._ingredient_names = {fields['name'] for fields in data}
        self._ingredient_units = {
            fields['measurement_unit'] for fields in data
        }
        self._bulk_create_ingredients(data=data)
        self._bulk_create_ingredient_amount(recipe=recipe, data=data)

    def _bulk_create_ingredients(self, data: list[dict]) -> None:
        ingredients_in_db = self._get_ingredient_in_db()
        valid_date = self._validate_ingredient_data(
            data=data, ingredients=ingredients_in_db
        )
        ingredients = [
            Ingredient(
                name=element['name'],
                measurement_unit=element['measurement_unit'],
            )
            for element in valid_date
        ]
        Ingredient.objects.bulk_create(ingredients)

    def _bulk_create_ingredient_amount(
        self, recipe: Recipe, data: list[dict]
    ) -> None:
        ingredients_in_db = self._get_ingredient_in_db()
        elements = [
            IngredientAmount(
                ingredient=self._get_valid_ingredient(
                    element=ingredient, ingredients_in_db=ingredients_in_db
                ),
                recipe=recipe,
                amount=ingredient['amount'],
            )
            for ingredient in data
        ]
        IngredientAmount.objects.bulk_create(elements)

    def _validate_ingredient_data(
        self, data: list[dict], ingredients: QuerySet
    ) -> list[dict]:
        valid_date = [
            element
            for element in data
            if not self._if_exist_ingredient(
                element=(element['name'], element['measurement_unit']),
                ingredients=self._transformation_ingredients(ingredients),
            )
        ]
        return valid_date

    def _get_ingredient_in_db(self) -> QuerySet:
        return Ingredient.objects.filter(
            name__in=self._ingredient_names,
            measurement_unit__in=self._ingredient_units,
        )

    @staticmethod
    def _if_exist_ingredient(
        ingredients: set[tuple],
        element: tuple,
    ) -> bool:
        return element in ingredients

    @staticmethod
    def _transformation_ingredients(ingredients: QuerySet) -> set[tuple]:
        return {
            (ingredient.name, ingredient.measurement_unit)
            for ingredient in ingredients
        }

    @staticmethod
    def _get_valid_ingredient(
        element: dict, ingredients_in_db: QuerySet
    ) -> Ingredient:
        return [
            ingredient
            for ingredient in ingredients_in_db
            if ingredient.name == element['name']
            and ingredient.measurement_unit == element['measurement_unit']
        ][0]
