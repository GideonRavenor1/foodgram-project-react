from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

User = get_user_model()


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(
    sender,
    instance: User = None,
    created: bool = False,
    **kwargs,
) -> None:
    """
    Автоматическое создание токена после создания супер-пользователя.
    """
    if created and instance.is_superuser:
        Token.objects.get_or_create(user=instance)
