from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Tag, Recipe, Ingredient, TagRecipe, IngredientsRecipe


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = (
        'username',
        'email',
        'avatar',
        'is_subscribed',
    )
    # search_fields = (
    #     'username',
    #     'first_name',
    #     'last_name',
    #     'email'
    # )
    # list_filter = (
    #     'role',
    #     'is_active',
    #     'is_staff'
    # )
    # fieldsets = (
    #     (None, {'fields': ('username', 'email', 'password')}),
    #     (
    #         'Персональная информация', {
    #             'fields': ('first_name', 'last_name', 'bio')
    #         }
    #     ),
    #     ('Разрешения',
    #      {'fields': ('role', 'is_active', 'is_staff', 'is_superuser')}),
    #     ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    # )
    # add_fieldsets = (
    #     (None, {
    #         'classes': ('wide',),
    #         'fields': ('username', 'email', 'password1', 'password2',
    #                    'role', 'is_staff', 'is_active')
    #     }),
    # )
    # list_editable = ('role',)
    ordering = ('username',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    pass


@admin.register(IngredientsRecipe)
class IngredientsRecipe(admin.ModelAdmin):
    list_display = (
        'ingredient',
        'recipe',
        'amount'
    )


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    pass
    # list_display = (
    #     'name',
    #     'year',
    #     'category',
    #     'genres',
    # )
    # list_editable = ('year', 'category')
    # filter_horizontal = ('genre',)

    # @admin.display(
    #     description='Жанры',
    # )
    # def genres(self, obj):
    #     return ",\n".join([g.name for g in obj.genre.all()])


@admin.register(TagRecipe)
class TagRecipe(admin.ModelAdmin):
    list_display = (
        'tag',
        'recipe',
    )
