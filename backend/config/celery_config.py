import os

from django.conf import settings
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery(main='FoodGramProject', include='recipes.tasks')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'get_recipes': {
        'task': 'recipes.tasks.get_recipes',
        'schedule': crontab(
            minute=0, hour=f'*/{settings.CELERY_BEAT_PER_HOUR}'
        ),
    },
}
