import base64

from django.core.files.base import ContentFile
from rest_framework import serializers

from .models import Tag, Recipe, Ingredient, TagRecipe, IngredientsRecipe, User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'is_subscribed',
            'avatar'
        )


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug')


class IngredientsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientsRecipeSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='ingredient.name')
    meansurement_unit = serializers.ReadOnlyField(source='ingredient.measurement_unit')

    class Meta:
        model = IngredientsRecipe
        fields = ('id', 'name', 'meansurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    ingredients = IngredientsRecipeSerializer(source='ingredientsrecipe_set', many=True, read_only=True)

    image = Base64ImageField()
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only='True'
    )

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_card', 'name', 'image', 'text', 'cooking_time',
        )

    def create(self, validated_data):
        ingredients = self.initial_data.pop('ingredients')
        tags = self.initial_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)

        for ingredient in ingredients:
            IngredientsRecipe.objects.create(
                ingredient_id=ingredient['id'], recipe=recipe, amount=ingredient['amount']
            )

        for tag in tags:
            TagRecipe.objects.create(
                tag_id=tag, recipe=recipe
            )
        return recipe
