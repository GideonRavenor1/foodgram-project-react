import os
import json

from django.apps.registry import Apps
from django.conf import settings
from django.db import migrations

DATA_DIR = os.path.join(settings.BASE_DIR.parent, 'data')


def get_data(path: str) -> list[dict]:
    with open(path, 'r', encoding='utf-8') as file:
        return json.load(file)


def add_ingredient_data(apps: Apps, *args, **kwargs) -> None:
    data = get_data(path=os.path.join(DATA_DIR, 'ingredients.json'))
    ingredient_model = apps.get_model(
        app_label='recipes', model_name='Ingredient'
    )
    ingredients = [ingredient_model(**fields) for fields in data]
    ingredient_model.objects.bulk_create(ingredients)


def delete_ingredient_data(apps: Apps, *args, **kwargs) -> None:
    data = get_data(path=os.path.join(DATA_DIR, 'ingredients.json'))
    ingredient_model = apps.get_model(
        app_label='recipes', model_name='Ingredient'
    )
    names = {fields['name'] for fields in data}
    measurement_units = {fields['measurement_unit'] for fields in data}
    ingredient_model.objects.filter(
        name__in=names, measurement_unit__in=measurement_units
    ).delete()


def add_tags_data(apps: Apps, *args, **kwargs) -> None:
    data = get_data(path=os.path.join(DATA_DIR, 'tags.json'))
    tags_model = apps.get_model(app_label='recipes', model_name='Tag')
    tags = [tags_model(**fields) for fields in data]
    tags_model.objects.bulk_create(tags)


def delete_tags_data(apps: Apps, *args, **kwargs) -> None:
    data = get_data(path=os.path.join(DATA_DIR, 'tags.json'))
    tags_model = apps.get_model(app_label='recipes', model_name='Tag')
    names = {fields['name'] for fields in data}
    tags_model.objects.filter(name__in=names).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_initial'),
    ]

    operations = [
        migrations.RunPython(
            add_ingredient_data, reverse_code=delete_ingredient_data
        ),
        migrations.RunPython(add_tags_data, reverse_code=delete_tags_data),
    ]
