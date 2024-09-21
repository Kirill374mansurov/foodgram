from djoser import views
from django_filters.rest_framework import DjangoFilterBackend
from requests import Response
from rest_framework import filters, viewsets, mixins, status
from rest_framework.decorators import action, permission_classes, api_view
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly,
                                        SAFE_METHODS)

from .models import Ingredient, IngredientsRecipe, Recipe, Tag, TagRecipe, User
from .serializers import TagSerializer, IngredientsSerializer, RecipeSerializer, UserSerializer


class UserViewSet(views.UserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination
    # filter_backends = [filters.SearchFilter]
    # search_fields = ['$username']
    # lookup_field = 'username'
    # http_method_names = ['get', 'post', 'patch', 'delete']

    # @action(detail=False, methods=['get'],
    #         permission_classes=[IsAuthenticated])
    # def me(self, request):
    #     serializer = self.get_serializer(request.user)
    #     print(serializer.data)
    #     return Response(serializer.data)

    # @me.mapping.patch
    # def patch_me(self, request):
    #     serializer = self.get_serializer(
    #         instance=request.user,
    #         data=request.data,
    #         partial=True
    #     )
    #     serializer.is_valid(raise_exceprion=True)
    #     serializer.save(role=request.user.role)
    #     return Response(serializer.data)


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
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    filterset_fields = ('name',)
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    # queryset = Recipe.objects.prefetch_related(
    #     'author', 'tags', 'ingredients').all()
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('author', 'is_favorited', 'is_in_shopping_cart', 'tags__slug')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
