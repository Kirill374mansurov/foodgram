from djoser import views
from django_filters.rest_framework import DjangoFilterBackend
from requests import Response
from rest_framework import filters, viewsets, mixins, status
from rest_framework.decorators import action, permission_classes, api_view
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from .filters import RecipeFilter
from .models import Ingredient, IngredientsRecipe, Recipe, Tag, TagRecipe, User
from .permissions import OwnerOrReadOnly, ReadOnly
from .serializers import TagSerializer, IngredientsSerializer, RecipeSerializer, UserSerializer


class UserViewSet(views.UserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    permission_classes = (ReadOnly,)

    @action(['get',], detail=False, url_path='me/avatar', permission_classes=(IsAuthenticated,))
    def me(self, request, *args, **kwargs):
        self.get_object = self.get_instance
        return self.retrieve(request, *args, **kwargs)

    @me.mapping.put
    def avatar(self, request):
        self.get_object = self.get_instance
        return self.update(request)


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
