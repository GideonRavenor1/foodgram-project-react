from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema, no_body
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from recipes.models.basic import Recipe
from recipes.models.m2m import Favorite, ShoppingCart
from ..filters import RecipeFilter
from ..permissions import IsAuthorOrReadOnly
from ..serializers.favorite import FavoriteSerializer
from ..serializers.recipes import (
    RecipeListSerializer,
    RecipeSerializer,
    ShortRecipeSerializer,
)
from ..serializers.shoping_cart import ShoppingCartSerializer
from ..services import get_list_ingredients
from ..logic import get_pdf


@method_decorator(
    name='create',
    decorator=swagger_auto_schema(
        request_body=RecipeSerializer(),
        responses={status.HTTP_201_CREATED: RecipeListSerializer()},
    ),
)
@method_decorator(
    name='update',
    decorator=swagger_auto_schema(
        request_body=RecipeSerializer(),
        responses={status.HTTP_201_CREATED: RecipeListSerializer()},
    ),
)
@method_decorator(
    name='partial_update',
    decorator=swagger_auto_schema(
        request_body=RecipeSerializer(),
        responses={status.HTTP_201_CREATED: RecipeListSerializer()},
    ),
)
@method_decorator(
    name='shopping_cart',
    decorator=swagger_auto_schema(
        request_body=no_body,
        responses={status.HTTP_201_CREATED: ShortRecipeSerializer()},
        tags=['ShoppingCart', 'Recipes'],
    ),
)
@method_decorator(
    name='delete_shopping_cart',
    decorator=swagger_auto_schema(tags=['ShoppingCart', 'Recipes']),
)
@method_decorator(
    name='favorite',
    decorator=swagger_auto_schema(
        request_body=no_body,
        responses={status.HTTP_201_CREATED: ShortRecipeSerializer()},
        tags=['Favorites', 'Recipes'],
    ),
)
@method_decorator(
    name='delete_favorite',
    decorator=swagger_auto_schema(tags=['Favorites', 'Recipes']),
)
@method_decorator(
    name='download_shopping_cart',
    decorator=swagger_auto_schema(
        operation_description='Скачать рецепт',
        responses={
            '200': openapi.Response(
                'File Attachment',
                schema=openapi.Schema(type=openapi.TYPE_FILE),
            )
        },
        tags=['Favorites', 'Recipes'],
    ),
)
class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    swagger_tags = ('Recipes',)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeListSerializer
        return RecipeSerializer

    @action(
        detail=True, methods=['POST'], permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk):
        return self.post_method_for_actions(
            request=request, pk=pk, serializers=FavoriteSerializer
        )

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        return self.delete_method_for_actions(
            request=request, pk=pk, model=Favorite
        )

    @action(
        detail=True, methods=['POST'], permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk):
        return self.post_method_for_actions(
            request=request, pk=pk, serializers=ShoppingCartSerializer
        )

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        return self.delete_method_for_actions(
            request=request, pk=pk, model=ShoppingCart
        )

    @action(
        detail=False, methods=['GET'], permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request) -> HttpResponse:
        ingredients = get_list_ingredients(user=request.user)
        content = get_pdf(context={'ingredients': ingredients})
        response = HttpResponse(
            content=content, content_type='application/pdf;'
        )
        response['Content-Disposition'] = 'inline; filename=shopping_list.pdf'
        response['Content-Transfer-Encoding'] = 'binary'
        return response

    @staticmethod
    def post_method_for_actions(request, pk, serializers):
        data = {'user': request.user.id, 'recipe': pk}
        serializer = serializers(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def delete_method_for_actions(request, pk, model):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        model_obj = get_object_or_404(model, user=user, recipe=recipe)
        model_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
