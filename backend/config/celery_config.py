import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery(main='FoodGramProject', include='recipes.tasks')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'get_recipes': {
        'task': 'Getting a random number of recipes every three hours',
        'schedule': crontab(minute=0, hour='*/3'),
    },
}
