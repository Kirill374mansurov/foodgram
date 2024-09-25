from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.urls import reverse
from shortuuid.django_fields import ShortUUIDField


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = (
        'username',
        'first_name',
        'last_name'
    )
    username = models.CharField(
        verbose_name='',
        max_length=150,
        unique=True,
        error_messages={
            'unique': 'Имя занято!',
        },
        validators=[UnicodeUsernameValidator()]
    )
    first_name = models.CharField(
        verbose_name='Имя', max_length=150
    )
    last_name = models.CharField(
        verbose_name='Фамилия', max_length=150
    )
    email = models.EmailField(
        verbose_name='Электронная почта',
        unique=True,
        error_messages={
            'unique': 'Почта занята!',
        },
        max_length=254
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
    name = models.CharField(max_length=32, verbose_name='Название')
    slug = models.SlugField(verbose_name='Слаг', null=True, max_length=32)

    class Meta(AbstractUser.Meta):
        ordering = ['name']
        verbose_name = 'тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=128, verbose_name='Название')
    measurement_unit = models.CharField(
        max_length=64,
        verbose_name='Единицы измерения'
    )

    class Meta(AbstractUser.Meta):
        ordering = ['name']
        verbose_name = 'ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
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
    name = models.CharField(max_length=128, verbose_name='Название')
    image = models.ImageField(
        upload_to='images/',
        null=True,
        default=None,
        verbose_name='Изображение'
    )
    text = models.CharField(max_length=256, verbose_name='Описание')
    cooking_time = models.IntegerField(
        verbose_name='Время приготовление в мин'
    )
    short_link = ShortUUIDField(
        length=4,
        max_length=8,
        prefix='http://127.0.0.1:8000/'
    )

    class Meta(AbstractUser.Meta):
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
        ordering = ['recipe', 'tag']
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
    amount = models.IntegerField(verbose_name='Количество')

    class Meta:
        ordering = ['recipe', 'ingredient']
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
        Recipe, on_delete=models.CASCADE, related_name='favorite')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='favorite')

    class Meta:
        ordering = ['recipe', 'user']
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
        Recipe, on_delete=models.CASCADE, related_name='shopping_cart'
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='shopping_cart'
    )

    class Meta:
        verbose_name = 'покупка списка'
        verbose_name_plural = 'Список покупок'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_user_recipe_in_cart')
        ]

    def __str__(self):
        return f'{self.user}: {self.recipe}'
