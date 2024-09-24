import base64

from django.core.files.base import ContentFile
from rest_framework import serializers

from .models import Tag, Recipe, Ingredient, TagRecipe, IngredientsRecipe, User, Favorite, Subscription


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'avatar'
        )
        lookup_field = 'username'

    def get_is_subscribed(self, obj):
        current_user = self.context.get('request').user
        return Subscription.objects.filter(author=obj, subscriber=current_user).exists()


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
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientsRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeLimitedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    ingredients = IngredientsRecipeSerializer(
        source='ingredientsrecipe_set',
        many=True,
        read_only=True
    )
    image = Base64ImageField(use_url=True)
    author = UserSerializer(
        read_only='True'
    )
    is_favorited = serializers.SerializerMethodField()
    # is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time',
        )

    def validate(self, data):
        for field in ('tags', 'ingredients'):
            if not self.initial_data.get(field):
                raise serializers.ValidationError(
                    f'Не заполнено поле `{field}`')
        ingredients = self.initial_data['ingredients']
        data_ingredients = Ingredient.objects.values_list('id', flat=True)
        ingredients_all = set()
        tags = self.initial_data['tags']
        data_tags = Tag.objects.values_list('id', flat=True)
        tags_all = []
        for ingredient in ingredients:
            if not ingredient.get('amount') or not ingredient.get('id'):
                raise serializers.ValidationError(
                    'Не все поля ингредиентов заполнены!')
            if ingredient['id'] not in data_ingredients:
                raise serializers.ValidationError(
                    'Несуществующий ингредиент!')
            if not int(ingredient['amount']) > 0:
                raise serializers.ValidationError(
                    'Неверное количество!')
            if ingredient['id'] in ingredients_all:
                raise serializers.ValidationError(
                    'Ингредиенты повторяются!')
            ingredients_all.add(ingredient['id'])

        for tag in tags:
            if tag in tags_all:
                raise serializers.ValidationError(
                    'Теги повторяются!')
            if tag not in data_tags:
                raise serializers.ValidationError(
                    'Несуществующий тег!')
            tags_all.append(tag)

        if not self.initial_data['cooking_time'] > 0:
            raise serializers.ValidationError(
                'Неверное время!')
        return data

    def create(self, validated_data):
        ingredients = self.initial_data.pop('ingredients')
        tags = self.initial_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)

        for ingredient in ingredients:
            IngredientsRecipe.objects.create(
                ingredient_id=ingredient['id'],
                recipe=recipe,
                amount=ingredient['amount']
            )

        for tag in tags:
            TagRecipe.objects.create(
                tag_id=tag,
                recipe=recipe
            )
        return recipe

    def get_is_favorited(self, obj):
        current_user = self.context['request'].user
        return Favorite.objects.filter(recipe=obj, user=current_user).exists()
