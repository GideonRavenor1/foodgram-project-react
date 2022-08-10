from rest_framework import serializers

from recipes.models.basic_models import Ingredient
from recipes.models.m2m_models import IngredientAmount


class IngredientSerializer(serializers.ModelSerializer):
    """
    Сериализатор ингредиентов
    """

    class Meta:
        model = Ingredient
        fields = '__all__'
        read_only_fields = '__all__'


class IngredientAmountSerializer(serializers.ModelSerializer):
    """
    Сериализатор вывода количества ингредиентов
    """

    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientAmount
        fields = ('id', 'name', 'measurement_unit', 'amount')


class CreateIngredientAmountSerializer(serializers.ModelSerializer):
    """
    Сериализатор добавления Ингредиентов
    """

    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientAmount
        fields = ('id', 'amount')

    def validate_amount(self, value):
        if int(value) <= 0:
            raise serializers.ValidationError(
                'Количество ингредиентов должно быть больше 0.'
            )
        return value
