from django.db import models
from django.core.validators import MinValueValidator

from .abstract_models import AbstractNamedModel


class Ingredient(AbstractNamedModel):
    measurement_unit = models.CharField(
        verbose_name='Единицы измерения',
        max_length=20,
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'], name='unique_ingredient'
            )
        ]
        app_label = 'recipes'

    def __str__(self):
        return f'{self.name} - {self.measurement_unit}'


class Tag(AbstractNamedModel):
    color = models.CharField(
        verbose_name='Цвет',
        max_length=7,
        help_text='Цветовой HEX-код',
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        unique=True,
        help_text='Неофициальное имя, часть URL адреса',
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
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
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        default_related_name = 'recipes'
        app_label = 'recipes'
