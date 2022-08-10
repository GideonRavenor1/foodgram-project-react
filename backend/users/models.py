from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Модель пользователя
    """

    email = models.EmailField(
        verbose_name='Электронная почта',
        max_length=254,
        unique=True,
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']


class Follow(models.Model):
    """
    Модель подписки.
    """

    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        verbose_name='Имя подписчика',
        related_name='follower',
        help_text='Выберите подписчика',
    )
    following = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        verbose_name='Имя автора',
        related_name='following',
        help_text='Выберите автора',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'user',
                    'following',
                ],
                name='follow_unique',
            )
        ]

    def clean(self) -> None:
        if self.user.username == self.following.username:
            raise ValidationError('Нельзя подписаться на самого себя')

    def __str__(self) -> str:
        return f'{self.user.username} - {self.following.username}'
