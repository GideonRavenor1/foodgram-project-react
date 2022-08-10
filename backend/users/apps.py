from django.apps import AppConfig
from django.core.signals import request_finished


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    verbose_name = 'Пользователи'

    def ready(self) -> None:
        """
        Запуск сигнала
        :return: None
        """

        from . import signals

        request_finished.connect(signals.create_auth_token)
