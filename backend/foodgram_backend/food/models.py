from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class Recipe(models.Model):
    pass
    # def __str__(self):
    #     return self.name


class Tag(models.Model):
    pass
    # def __str__(self):
    #     return self.name


class Ingredient(models.Model):
    pass
    # def __str__(self):
    #     return f'{self.achievement} {self.cat}'
