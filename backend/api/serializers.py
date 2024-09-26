import base64

from django.core.files.base import ContentFile
from rest_framework import serializers

from backend import constants
from .models import (Favorite, Ingredient, IngredientsRecipe, Recipe,
                     ShoppingCart, Subscription, TagRecipe, Tag, User)


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

    # def validate(self, data):
    #     print(data['subscriber'])
    #     if data['subscriber'] == data['author']:
    #         raise serializers.ValidationError(
    #             'Нельзя подписаться на себя!'
    #         )
    #     return data

    def get_is_subscribed(self, obj):
        current_user = self.context.get('request').user.id
        # return Subscription.objects.filter(
        #     author=obj, subscriber=current_user
        # ).exists()
        return User.objects.get(username=obj).subscription.all().exists()


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
    amount = serializers.IntegerField(
        max_value=constants.MAX_AMOUNT, min_value=constants.MIN_AMOUNT
    )

    class Meta:
        model = IngredientsRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSmallSerializer(serializers.ModelSerializer):

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
    is_in_shopping_cart = serializers.SerializerMethodField()
    cooking_time = serializers.IntegerField(
        max_value=constants.COOKING_TIME_MAX,
        min_value=constants.COOKING_TIME_MIN
    )

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time'
        )

    def validate(self, data):
        if not self.initial_data.get('tags'):
            raise serializers.ValidationError(
                f'Не заполнено поле tags'
            )
        if not self.initial_data.get('ingredients'):
            raise serializers.ValidationError(
                f'Не заполнено поле ingredients'
            )
        ingredients = self.initial_data['ingredients']
        data_ingredients = set(Ingredient.objects.values_list('id', flat=True))
        ingredients_ids = set()
        tags = self.initial_data['tags']
        data_tags = set(Tag.objects.values_list('id', flat=True))
        for ingredient in ingredients:
            # if not ingredient.get('amount') or not ingredient.get('id'):
            #     raise serializers.ValidationError(
            #         'Не все поля ингредиентов заполнены!'
            #     )
            if ingredient['id'] not in data_ingredients:
                raise serializers.ValidationError(
                    'Несуществующий ингредиент!'
                )
            # if not int(ingredient['amount']) > 0:
            #     raise serializers.ValidationError(
            #         'Неверное количество!'
            #     )
            if ingredient['id'] in ingredients_ids:
                raise serializers.ValidationError(
                    'Ингредиенты повторяются!'
                )
            ingredients_ids.add(ingredient['id'])

        tags_ids = set()
        for tag in tags:
            if tag in tags_ids:
                raise serializers.ValidationError(
                    'Теги повторяются!'
                )
            if tag not in data_tags:
                raise serializers.ValidationError(
                    'Несуществующий тег!'
                )
            tags_ids.add(tag)

        # if not self.initial_data['cooking_time'] > 0:
        #     raise serializers.ValidationError(
        #         'Неверное время!'
        #     )
        return data

    def create(self, validated_data):
        ingredients = self.initial_data.pop('ingredients')
        tags = self.initial_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)

        obj = (IngredientsRecipe(
            recipe=recipe, ingredient_id=ing['id'], amount=ing['amount']
        ) for ing in ingredients)
        IngredientsRecipe.objects.bulk_create(obj)

        # for tag in tags:
        #     TagRecipe.objects.create(
        #         tag_id=tag,
        #         recipe=recipe
        #     )
        obj = (TagRecipe(
            recipe=recipe, tag_id=tag
        ) for tag in tags)
        TagRecipe.objects.bulk_create(obj)

        return recipe

    def update(self, instance, validated_data):
        ingredients = self.initial_data.pop('ingredients')
        IngredientsRecipe.objects.filter(recipe=instance).all().delete()

        obj = (IngredientsRecipe(
            recipe=instance, ingredient_id=ing['id'], amount=ing['amount']
        ) for ing in ingredients)
        IngredientsRecipe.objects.bulk_create(obj)

        tags = self.initial_data.get('tags')
        obj = (TagRecipe(
            recipe=instance, tag_id=tag
        ) for tag in tags)
        TagRecipe.objects.bulk_create(obj)
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time)
        instance.save()
        return instance

    def get_is_favorited(self, obj):
        current_user = self.context['request'].user.id
        return Favorite.objects.filter(recipe=obj, user=current_user).exists()
        # Recipe.objects.get(name=obj)
        # return True

    def get_is_in_shopping_cart(self, obj):
        current_user = self.context['request'].user.id
        return ShoppingCart.objects.filter(
            recipe=obj, user=current_user
        ).exists()
        # return User.objects.get(username=obj).shopping_cart.all().exists()


class SubscriptionSerializer(UserSerializer):
    recipes_count = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ('recipes', 'recipes_count',)

    # def validate(self, data):
    #     print(data['subscriber'])
    #     if data['subscriber'] == data['author']:
    #         raise serializers.ValidationError(
    #             'Нельзя подписаться на себя!'
    #         )
    #     return data

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        recipes = Recipe.objects.filter(author=obj)
        # recipes = User.objects.get(username=obj).recipes.all()
        if limit:
            recipes = recipes[:int(limit)]
        return RecipeSmallSerializer(recipes, many=True).data
