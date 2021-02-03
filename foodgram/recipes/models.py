from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField
from django.shortcuts import reverse

User = get_user_model()


class Recipe(models.Model):
    title = models.TextField(blank=True)
    ingredients = JSONField(null=True)
    pub_date = models.DateTimeField("date published", auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="recipes")
    diets = models.ManyToManyField(
        'Diet', blank=True, related_name="recipe_set", verbose_name="рацион")
    description = models.TextField(blank=True)
    cooking_time = models.IntegerField()
    image = models.ImageField(upload_to='recipec/', blank=True, null=True)

    def get_absolute_url(self):
        return f'/{self.author}/'

    class Meta:
        ordering = ["-pub_date"]


class Diet(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)

    def get_absolute_url(self):
        return reverse('filter', args=[str(self.slug)])

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["title"]


class FollowUser(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='follower')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following')


class FollowRecipe(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="followers_recipe")
    following_recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="following_recipe")
    is_favore = models.BooleanField(default=False)


class Purchases(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='user_shoping_list')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='recipe_shoping_list')


class UnitIngredients(models.Model):
    ingredients_unit = models.CharField(max_length=200)
    dimension_unit = models.CharField(max_length=200)


class Tag(models.Model):
    demension = models.CharField(max_length=200)
