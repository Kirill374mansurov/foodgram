import os

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse
from shortuuid.django_fields import ShortUUIDField

from backend import constants


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = (
        'username',
        'first_name',
        'last_name'
    )
    username = models.CharField(
        verbose_name='',
        max_length=constants.NAME_MAX_LENGHT,
        unique=True,
        error_messages={
            'unique': 'Имя занято!',
        },
        validators=[UnicodeUsernameValidator()]
    )
    first_name = models.CharField(
        verbose_name='Имя', max_length=constants.NAME_MAX_LENGHT
    )
    last_name = models.CharField(
        verbose_name='Фамилия', max_length=constants.NAME_MAX_LENGHT
    )
    email = models.EmailField(
        verbose_name='Электронная почта',
        unique=True,
        error_messages={
            'unique': 'Почта занята!',
        },
        max_length=constants.EMAIL_MAX_LENGHT
    )
    avatar = models.ImageField(
        null=True,
        blank=True,
        verbose_name='Аватар'
    )
    is_subscribed = models.BooleanField(
        default=False,
        verbose_name='Подписка'
    )

    class Meta(AbstractUser.Meta):
        ordering = ['username']
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Subscription(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='subscription'
    )
    subscriber = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Подписчик',
        related_name='subscriber'
    )

    class Meta:
        ordering = ['author']
        verbose_name = 'подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'subscriber'],
                name='unique_author_subscriber'
            )
        ]

    def __str__(self):
        return f'{self.author}: {self.subscriber}'


class Tag(models.Model):
    name = models.CharField(
        max_length=constants.TAG_MAX_LENGHT, verbose_name='Название'
    )
    slug = models.SlugField(
        verbose_name='Слаг', null=True, max_length=constants.TAG_MAX_LENGHT
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=constants.INGREDIENT_NAME_MAX_LENGHT,
        verbose_name='Название'
    )
    measurement_unit = models.CharField(
        max_length=constants.MEASUREMENT_UNIT_MAX_LENGHT,
        verbose_name='Единицы измерения'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='recipes'
    )
    tags = models.ManyToManyField(
        Tag,
        through='TagRecipe'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientsRecipe'
    )
    is_favorited = models.BooleanField(
        default=False,
        verbose_name='В избранном'
    )
    is_in_shopping_cart = models.BooleanField(
        default=False,
        verbose_name='В списке покупок'
    )
    name = models.CharField(
        max_length=constants.RECEPT_NAME_MAX_LENGHT, verbose_name='Название'
    )
    image = models.ImageField(
        upload_to='images/',
        null=True,
        default=None,
        verbose_name='Изображение'
    )
    text = models.CharField(
        max_length=constants.TEXT_MAX_LENGHT, verbose_name='Описание'
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовление в мин',
        validators=[
            MinValueValidator(constants.COOKING_TIME_MIN),
            MaxValueValidator(constants.COOKING_TIME_MAX)
        ]
    )
    short_link = ShortUUIDField(
        length=constants.SHORT_LINK_LENGHT,
        max_length=constants.SHORT_LINK_MAX_LENGHT,
        prefix=os.getenv('ALLOWED_HOST')
    )

    class Meta:
        default_related_name = 'recipes'
        ordering = ['name']
        verbose_name = 'рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('recipe-detail', kwargs={'recipe_id': self.pk})


class TagRecipe(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, verbose_name='Тег')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, verbose_name='рецепт'
    )

    class Meta:
        ordering = ['recipe']
        verbose_name = 'тег рецепта'
        verbose_name_plural = 'Теги рецептов'
        constraints = [
            models.UniqueConstraint(
                fields=['tag', 'recipe'], name='unique_tag_recipe'
            )
        ]

    def __str__(self):
        return f'{self.recipe}: {self.tag}'


class IngredientsRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, verbose_name='Ингредиенты'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, verbose_name='рецепт'
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        validators=[
            MinValueValidator(constants.MIN_AMOUNT),
            MaxValueValidator(constants.MAX_AMOUNT)
        ]
    )

    class Meta:
        ordering = ['recipe']
        verbose_name = 'ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецептов'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_ingredient_recipe'
            )
        ]

    def __str__(self):
        return f'{self.recipe}: {self.ingredient}'


class Favorite(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='Рецепт'
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='Пользователь'
    )

    class Meta:
        ordering = ['user']
        verbose_name = 'избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique_user_favorite_recipe'
            )
        ]

    def __str__(self):
        return f'{self.user}: {self.recipe}'


class ShoppingCart(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Рецепт'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Пользователь'
    )

    class Meta:
        ordering = ['user']
        verbose_name = 'покупка списка'
        verbose_name_plural = 'Список покупок'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_user_recipe_in_cart')
        ]

    def __str__(self):
        return f'{self.user}: {self.recipe}'
