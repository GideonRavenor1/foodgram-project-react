import random

import requests
from django.conf import settings
from django.contrib.auth import get_user_model

from config.celery_config import app
from .models.basic import Tag
from .services import RecipesCrawler, JsonParser, RecipeSaver

User = get_user_model()


@app.task(
    name='recipes.tasks.get_recipes',
    bind=True,
    retry_backoff=600,
    retry_jitter=True,
    max_retries=settings.CELERY_RETRY_COUNT,
)
def get_recipes(self):
    tag = random.choice(Tag.objects.all().values_list('slug', flat=True))
    crawler = RecipesCrawler(tag=tag)
    try:
        crawler.execute()
    except requests.HTTPError as error:
        raise self.retry(exc=error)

    data = crawler.result
    parser = JsonParser(data=data, tag=tag)
    parser.parse()
    result = parser.result
    saver = RecipeSaver(data=result)
    number_of_recipes_created = saver.save()
    if not number_of_recipes_created:
        raise self.retry(exc=ValueError('Не одного рецепта не создано'))
    return {
        'status': 'successfully',
        'detail': f'Number of recipes created: {number_of_recipes_created}',
    }
