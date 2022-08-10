from rest_framework import serializers

from recipes.models.basic_models import Tag


class TagSerializer(serializers.ModelSerializer):
    """
    Сериализатор тегов
    """

    class Meta:
        model = Tag
        fields = '__all__'
        read_only_fields = '__all__'
