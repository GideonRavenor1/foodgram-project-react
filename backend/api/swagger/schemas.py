from drf_yasg import openapi
from drf_yasg.app_settings import swagger_settings
from drf_yasg.inspectors import SwaggerAutoSchema, FieldInspector


class Base64FileFieldInspector(FieldInspector):
    BASE_64_FIELDS = [
        'Base64ImageField',
        'Base64FileField',
        'Base64FieldMixin',
    ]

    def __classlookup(self, cls):
        c = list(cls.__bases__)
        for base in c:
            c.extend(self.__classlookup(base))
        return c

    def process_result(self, result, method_name, obj, **kwargs):
        if isinstance(result, openapi.Schema.OR_REF):
            base_classes = [
                x.__name__ for x in self.__classlookup(obj.__class__)
            ]
            if any(
                item in Base64FileFieldInspector.BASE_64_FIELDS
                for item in base_classes
            ):
                schema = openapi.resolve_ref(result, self.components)
                schema.pop('readOnly', None)
                schema.pop('format', None)

        return result


class CustomAutoSchema(SwaggerAutoSchema):
    """
    Переопределенный кастомный класс SwaggerAutoSchema,
    позволяющий явно указывать теги и корректно отображающий поле Base64.
    """

    field_inspectors = [
        Base64FileFieldInspector
    ] + swagger_settings.DEFAULT_FIELD_INSPECTORS

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
