from rest_framework import serializers

from recipes.models.basic import Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

    def get_fields(self) -> dict:
        fields = super().get_fields()
        for field in fields.values():
            field.read_only = True
        return fields
