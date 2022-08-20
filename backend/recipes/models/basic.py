from colorfield.fields import ColorField
from django.core.validators import MinValueValidator
from django.db import models

from .abstract import AbstractNamedModel

DEFAULT_COLOR_CODE = '#FF0000'


class Ingredient(AbstractNamedModel):
    measurement_unit = models.CharField(
        verbose_name='Единицы измерения',
        max_length=20,
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(
                fields=(
                    'name',
                    'measurement_unit',
                ),
                name='unique_ingredient',
            ),
        ]
        app_label = 'recipes'

    def __str__(self):
        return f'{self.name} - {self.measurement_unit}'


class Tag(AbstractNamedModel):
    color = ColorField(
        verbose_name='Цвет',
        default=DEFAULT_COLOR_CODE,
        help_text='Цветовой HEX-код',
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        help_text='Укажите имя тега в переводе на английский язык.',
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        constraints = [
            models.UniqueConstraint(
                fields=('name',),
                name='unique_tag_name',
            ),
            models.UniqueConstraint(
                fields=('slug',),
                name='unique_tag_slug',
            ),
        ]
        app_label = 'recipes'


class Recipe(AbstractNamedModel):
    author = models.ForeignKey(
        to='users.User',
        on_delete=models.CASCADE,
        verbose_name='Автор рецепта',
    )
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='recipes/',
    )
    text = models.TextField(verbose_name='Описание рецепта')
    ingredients = models.ManyToManyField(
        to=Ingredient,
        verbose_name='Ингредиенты',
        through='recipes.IngredientAmount',
    )
    tags = models.ManyToManyField(
        to=Tag,
        verbose_name='Теги',
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        validators=[
            MinValueValidator(
                limit_value=1, message='Время должно быть больше 1 минуты'
            )
        ],
        help_text='Время приготовления в минутах',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        default_related_name = 'recipes'
        constraints = [
            models.UniqueConstraint(
                fields=('name',),
                name='unique_recipe_name',
            ),
        ]
        app_label = 'recipes'
