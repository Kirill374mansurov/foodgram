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
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects)
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientsRecipe
        fields = ('id', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects)
    ingredients = IngredientsRecipeSerializer(many=True)

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
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        for ingredient in ingredients:
            IngredientsRecipe.objects.create(
                ingredient=ingredient['id'], recipe=recipe, amount=ingredient['amount']
            )
        for tag in tags:
            TagRecipe.objects.create(
                tag=tag, recipe=recipe
            )
        return recipe
