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

    class Meta:
        model = Recipe
        fields = ('tags', 'author')
