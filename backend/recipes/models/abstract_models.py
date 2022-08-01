from django.db import models


class AbstractNamedModel(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название',
        unique=True,
    )

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.name


class AbstractUserRelationModel(models.Model):
    user = models.ForeignKey(
        to='users.User',
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        to='recipes.Recipe',
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return f'{self.user.email} {self.recipe.name}'
