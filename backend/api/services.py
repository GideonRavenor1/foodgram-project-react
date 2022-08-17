from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.db.models import F, Sum

from recipes.models.m2m import IngredientAmount


User = get_user_model()


def get_list_ingredients(user: User) -> QuerySet:

    ingredients = (
        IngredientAmount.objects.filter(recipe__carts__user=user)
        .values(
            name=F('ingredient__name'),
            measurement_unit=F('ingredient__measurement_unit'),
        )
        .annotate(amount=Sum('amount'))
        .values_list(
            'ingredient__name', 'amount', 'ingredient__measurement_unit'
        )
    )
    return ingredients
