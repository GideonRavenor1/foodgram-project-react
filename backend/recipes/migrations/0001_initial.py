# Generated by Django 4.0.6 on 2022-08-15 09:29

import colorfield.fields
import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Favorite',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Избранное',
                'verbose_name_plural': 'Избранные',
                'default_related_name': 'favorites',
            },
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'name',
                    models.CharField(max_length=256, verbose_name='Название'),
                ),
                (
                    'measurement_unit',
                    models.CharField(
                        max_length=20, verbose_name='Единицы измерения'
                    ),
                ),
            ],
            options={
                'verbose_name': 'Ингредиент',
                'verbose_name_plural': 'Ингредиенты',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='IngredientAmount',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'amount',
                    models.PositiveSmallIntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(
                                limit_value=1,
                                message='Количество не может быть меньше 1',
                            )
                        ],
                        verbose_name='Количество ингредиента',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Количество ингредиента',
                'verbose_name_plural': 'Количество ингредиентов',
                'default_related_name': 'amounts',
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'name',
                    models.CharField(max_length=256, verbose_name='Название'),
                ),
                (
                    'image',
                    models.ImageField(
                        upload_to='recipes/', verbose_name='Изображение'
                    ),
                ),
                ('text', models.TextField(verbose_name='Описание рецепта')),
                (
                    'cooking_time',
                    models.PositiveSmallIntegerField(
                        help_text='Время приготовления в минутах',
                        validators=[
                            django.core.validators.MinValueValidator(
                                limit_value=1,
                                message='Время должно быть больше 1 минуты',
                            )
                        ],
                        verbose_name='Время приготовления',
                    ),
                ),
                (
                    'pub_date',
                    models.DateTimeField(
                        auto_now_add=True, verbose_name='Дата публикации'
                    ),
                ),
            ],
            options={
                'verbose_name': 'Рецепт',
                'verbose_name_plural': 'Рецепты',
                'ordering': ('-pub_date',),
                'default_related_name': 'recipes',
            },
        ),
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Список покупок',
                'verbose_name_plural': 'Списки покупок',
                'default_related_name': 'carts',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'name',
                    models.CharField(max_length=256, verbose_name='Название'),
                ),
                (
                    'color',
                    colorfield.fields.ColorField(
                        default='#FF0000',
                        help_text='Цветовой HEX-код',
                        image_field=None,
                        max_length=18,
                        samples=None,
                        verbose_name='Цвет',
                    ),
                ),
                (
                    'slug',
                    models.SlugField(
                        help_text='Укажите имя тега в переводе на английский язык',
                        verbose_name='Слаг',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
                'ordering': ('name',),
            },
        ),
        migrations.AddConstraint(
            model_name='tag',
            constraint=models.UniqueConstraint(
                fields=('name',), name='unique_tag_name'
            ),
        ),
        migrations.AddConstraint(
            model_name='tag',
            constraint=models.UniqueConstraint(
                fields=('slug',), name='unique_tag_slug'
            ),
        ),
        migrations.AddField(
            model_name='shoppingcart',
            name='recipe',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to='recipes.recipe',
                verbose_name='Рецепт',
            ),
        ),
    ]
