import base64
from collections import defaultdict

from djoser import views
from django.core.files.base import ContentFile
from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse

from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .filters import RecipeFilter
from .models import (Favorite, Ingredient, IngredientsRecipe, Recipe,
                     ShoppingCart, Subscription, Tag, User)
from .permissions import OwnerOrReadOnly, ReadOnly
from .serializers import (IngredientsSerializer, RecipeSerializer,
                          RecipeSmallSerializer, SubscriptionSerializer,
                          TagSerializer, UserSerializer)


class UserViewSet(views.UserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (ReadOnly,)

    @action(
        ['get'], detail=False, permission_classes=(IsAuthenticated,)
    )
    def me(self, request, *args, **kwargs):
        self.get_object = self.get_instance
        return self.retrieve(request, *args, **kwargs)

    @action(
        ['put', 'delete'],
        url_path='me/avatar',
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def avatar(self, request):
        avatar = request.user.avatar

        if request.method == 'DELETE':
            avatar.delete(save=True)
            return Response(status=status.HTTP_204_NO_CONTENT)

        new_avatar = request.data.get('avatar')
        if not new_avatar:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        avatar_format, avatar_base64 = new_avatar.split(';base64,')
        extension = avatar_format.split('/')[-1]
        filename = f"{request.user.username}.{extension}"
        data = ContentFile(base64.b64decode(avatar_base64), name=filename)

        avatar.save(filename, data)
        return Response(
            {'avatar': avatar.url},
            status=status.HTTP_200_OK
        )

    @action(methods=['post', 'delete'], detail=True,
            permission_classes=[IsAuthenticated])
    def subscribe(self, request, id):
        author = get_object_or_404(User, pk=id)

        if request.method == 'DELETE':
            try:
                subscription = Subscription.objects.get(
                    author=author, subscriber=request.user
                )
                subscription.delete()
            except BaseException:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_204_NO_CONTENT)

        if request.user == author:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        self.serializer_class = SubscriptionSerializer
        created = Subscription.objects.get_or_create(
            author=author, subscriber=request.user)
        if not created[-1]:
            return Response(
                {'errors': 'Уже подписаны!'},
                status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(
            author, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['get'], detail=False,
            permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        self.serializer_class = SubscriptionSerializer
        authors = User.objects.filter(subscription__subscriber=request.user)
        page = self.paginate_queryset(authors)
        if page is not None:
            serializer = self.get_serializer(
                page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(
            authors, many=True, context={'request': request})
        return Response(serializer.data)


class RetrieveListViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                          viewsets.GenericViewSet):
    pass


class TagViewSet(RetrieveListViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(RetrieveListViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientsSerializer
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name',)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (OwnerOrReadOnly,)
    serializer_class = RecipeSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    filterset_fields = (
        'is_favorited', 'is_in_shopping_cart'
    )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        methods=['get'],
        detail=True,
        permission_classes=(ReadOnly,),
        url_path='get-link'
    )
    def get_link(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        return Response(
            {'short-link': recipe.short_link},
            status=status.HTTP_200_OK
        )

    @action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, pk):
        if request.method == 'POST':
            recipe = get_object_or_404(Recipe, pk=pk)
            created = Favorite.objects.get_or_create(
                recipe=recipe, user=request.user
            )
            if not created[-1]:
                return Response(
                    {'errors': 'Рецепт уже в избранном!'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer = RecipeSmallSerializer(
                recipe, context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        recipe = get_object_or_404(Recipe, pk=pk)
        try:
            fav_recipe = Favorite.objects.get(recipe=recipe, user=request.user)
            fav_recipe.delete()
        except BaseException:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk):
        if request.method == 'DELETE':
            recipe = get_object_or_404(Recipe, pk=pk)
            try:
                fav_recipe = ShoppingCart.objects.get(
                    recipe=recipe, user=request.user
                )
                fav_recipe.delete()
            except BaseException:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_204_NO_CONTENT)

        recipe = get_object_or_404(Recipe, pk=pk)
        created = ShoppingCart.objects.get_or_create(
            recipe=recipe, user=request.user)
        if not created[-1]:
            return Response(
                {'errors': 'Рецепт уже добавлен!'},
                status.HTTP_400_BAD_REQUEST
            )
        serializer = RecipeSmallSerializer(
            recipe, context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['get'], detail=False,
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        ingredients = IngredientsRecipe.objects.filter(
            recipe__shopping_cart__user=request.user).values(
                'ingredient__name',
                'ingredient__measurement_unit',
                'amount').order_by('ingredient__name')

        data = defaultdict(int)
        for ingr in ingredients:
            key = (
                f'{ingr["ingredient__name"]} '
                f'({ingr["ingredient__measurement_unit"]})'
            )
            data[key] += ingr['amount']
        shopping_list = ['СПИСОК ПОКУПОК:\n']
        for key, value in data.items():
            shopping_list.append(f'- {key}: {value} \n')

        response = HttpResponse(shopping_list, content_type='text/plain')
        response['Content-Disposition'] = (
            'attachment; filename={0}'.format('shopping_list.txt')
        )
        return response
