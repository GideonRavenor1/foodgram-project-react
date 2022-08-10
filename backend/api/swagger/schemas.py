from drf_yasg.inspectors import SwaggerAutoSchema


class CustomAutoSchema(SwaggerAutoSchema):
    """
    Переопределенный кастомный класс SwaggerAutoSchema,
    позволяющий явно указывать теги.
    """

    def get_tags(self, operation_keys=None):
        """
        Переопределенный метод get_tags, позволяет добавлять имена тагов
        по полю swagger_tags.
        """

        tags = self.overrides.get('tags', None) or getattr(
            self.view,
            'swagger_tags',
            [],
        )

        if not tags:
            tags = [operation_keys[0]]

        return tags
