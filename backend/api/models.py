from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator


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
        validators=[UnicodeUsernameValidator(),]
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
    is_in_shopping_card = models.BooleanField(
        default=False,
        verbose_name='В списке покупок'
    )
    name = models.CharField(max_length=128, verbose_name='Название')
    image = models.ImageField(
        upload_to='food/images/',
        null=True,
        default=None,
        verbose_name='Изображение'
    )
    text = models.CharField(max_length=256, verbose_name='Описание')
    cooking_time = models.IntegerField(
        verbose_name='Время приготовление в мин'
    )

    class Meta(AbstractUser.Meta):
        ordering = ['name']
        verbose_name = 'рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name

class TagRecipe(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, verbose_name='Тег')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name='рецепт')


class IngredientsRecipe(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, verbose_name='Ингредиенты')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name='рецепт')
    amount = models.IntegerField(verbose_name='Количество')
