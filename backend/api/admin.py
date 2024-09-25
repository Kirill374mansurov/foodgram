from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (Ingredient, IngredientsRecipe,
                     Recipe, Tag, TagRecipe, User)


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = (
        'username',
        'email',
        'avatar',
        'is_subscribed',
    )
    ordering = ('username',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    pass


class IngredientsRecipeAdmin(admin.StackedInline):
    model = IngredientsRecipe
    extra = 0
    verbose_name = 'ингредиент'
    verbose_name_plural = 'Ингредиенты'


class TagRecipeAdmin(admin.StackedInline):
    model = TagRecipe
    extra = 0
    verbose_name = 'тег'
    verbose_name_plural = 'Теги'


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'text',
        'get_tags',
        'get_ingredients'
    )
    inlines = (
        IngredientsRecipeAdmin,
        TagRecipeAdmin
    )

    @admin.display(
        description='Теги',
    )
    def get_tags(self, obj):
        return ",\n".join([g.name for g in obj.tags.all()])

    @admin.display(
        description='Ингредиенты',
    )
    def get_ingredients(self, obj):
        return ",\n".join([g.name for g in obj.ingredients.all()])
