from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request

from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import Follow
from ..serializers.follows import FollowSerializer


User = get_user_model()


class FollowAPIView(APIView):
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]
    swagger_tags = ('Follows',)

    @swagger_auto_schema(
        responses={status.HTTP_201_CREATED: FollowSerializer()}
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        subscriber = get_object_or_404(User, id=self.kwargs.get('user_id'))
        if subscriber == request.user:
            return Response(
                {'error': 'Нельзя подписаться на самого себя'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if Follow.objects.filter(
            user=request.user, following=subscriber
        ).exists():
            return Response(
                {'error': 'Вы уже подписаны на этого пользователя'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        Follow.objects.create(user=request.user, following=subscriber)
        return Response(
            self.serializer_class(
                subscriber, context={'request': request}
            ).data,
            status=status.HTTP_201_CREATED,
        )

    def delete(self, request: Request, *args, **kwargs) -> Response:
        subscriber = get_object_or_404(User, id=self.kwargs.get('user_id'))
        subscription = Follow.objects.filter(
            user=request.user, following=subscriber
        )
        if subscription:
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'error': 'Вы не подписаны на этого пользователя'},
            status=status.HTTP_400_BAD_REQUEST,
        )


class FollowListAPIView(ListAPIView):
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]
    swagger_tags = ('Follows',)

    def get_queryset(self) -> list[User]:
        return User.objects.filter(followers__user=self.request.user)
