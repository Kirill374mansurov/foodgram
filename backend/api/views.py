from rest_framework import viewsets
from rest_framework import mixins
from djoser import views

from .models import Ingredient, IngredientsRecipe, Recipe, Tag, TagRecipe, User
from .serializers import TagSerializer, IngredientsSerializer, RecipeSerializer, UserSerializer


class UserViewSet(views.UserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RetrieveListViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                          viewsets.GenericViewSet):
    pass


class TagViewSet(RetrieveListViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(RetrieveListViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientsSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
