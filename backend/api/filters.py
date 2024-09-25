from django_filters import rest_framework

from .models import Recipe, Tag, User


class RecipeFilter(rest_framework.FilterSet):
    tags = rest_framework.filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags__slug',
        to_field_name='slug'
    )
    author = rest_framework.filters.ModelMultipleChoiceFilter(
        queryset=User.objects.all(),
        field_name='author__id',
        to_field_name='id'
    )
    is_favorited = rest_framework.filters.BooleanFilter(
        field_name='is_favorited', method='filter_bool')
    is_in_shopping_cart = rest_framework.filters.BooleanFilter(
        field_name='is_in_shopping_cart', method='filter_bool')

    class Meta:
        model = Recipe
        fields = ('tags', 'author')

    def filter_bool(self, queryset, name, value):
        if self.request.user.is_anonymous:
            return queryset
        if name == 'is_in_shopping_cart' and value:
            return queryset.filter(
                shopping_cart__user=self.request.user)
        if name == 'is_favorited' and value:
            return queryset.filter(
                favorite__user=self.request.user)
        return queryset
