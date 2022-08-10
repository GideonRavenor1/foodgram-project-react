import os
import json

from django.apps.registry import Apps
from django.conf import settings
from django.db import migrations, models

DATA_FILE = os.path.join(settings.BASE_DIR.parent, 'data/ingredients.json')


def add_ingredient_data(apps: Apps, *args, **kwargs) -> None:
    data = get_ingredient_data()
    ingredient_model = apps.get_model(
        app_label='recipes', model_name='Ingredient'
    )
    ingredients = [ingredient_model(**fields) for fields in data]
    ingredient_model.objects.bulk_create(ingredients)


def get_ingredient_data() -> list[dict]:
    with open(DATA_FILE, 'r', encoding='utf-8') as file:
        return json.load(file)


def delete_ingredient_data(apps: Apps, *args, **kwargs) -> None:
    data = get_ingredient_data()
    ingredient_model = apps.get_model(
        app_label='recipes', model_name='Ingredient'
    )
    names = {fields['name'] for fields in data}
    measurement_units = {fields['measurement_unit'] for fields in data}
    ingredient_model.objects.filter(
        name__in=names, measurement_unit__in=measurement_units
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_initial'),
    ]

    operations = [
        migrations.RunPython(
            add_ingredient_data, reverse_code=delete_ingredient_data
        )
    ]
