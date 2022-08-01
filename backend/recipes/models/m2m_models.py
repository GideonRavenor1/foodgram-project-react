from django.core.validators import MinValueValidator
from django.db import models

from .abstract_models import AbstractUserRelationModel


class Favorite(AbstractUserRelationModel):
    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique_favorite'
            )
        ]
        app_label = 'recipes'


class ShoppingCart(AbstractUserRelationModel):
    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shopping_cart',
            )
        ]
        app_label = 'recipes'


class IngredientAmount(models.Model):
    recipe = models.ForeignKey(
        to='recipes.Recipe', on_delete=models.CASCADE, verbose_name='Рецепт'
    )
    ingredient = models.ForeignKey(
        to='recipes.Ingredient',
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество ингредиента',
        validators=[
            MinValueValidator(
                limit_value=1, message='Количество не может быть меньше 1'
            )
        ],
    )

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'
        constraints = (
            models.UniqueConstraint(
                fields=(
                    'ingredient',
                    'recipe',
                ),
                name='unique_ingredient_amount',
            ),
        )
        default_related_name = 'amounts'
        app_label = 'recipes'

    def __str__(self) -> str:
        return f'{self.recipe.name} {self.ingredient.name} {self.ingredient.measurement_unit}'
