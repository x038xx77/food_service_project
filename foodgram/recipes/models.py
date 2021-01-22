from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField
from django.shortcuts import reverse

User = get_user_model()


class Diet(models.Model):
    title = models.CharField(max_length=7)
    slug = models.SlugField(unique=True)

    def get_absolute_url(self):
        return reverse('filter', args=[str(self.slug)])

    def __str__(self):
        return self.title


class Recipe(models.Model):
    title = models.TextField(blank=True)
    ingredients = JSONField(null=True)
    pub_date = models.DateTimeField("date published", auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="recipes")
    diet = models.ForeignKey(
        Diet, on_delete=models.SET_NULL,
        related_name="diet", blank=True, null=True, verbose_name="рацион")
    description = models.TextField(blank=True)
    cooking_time = models.IntegerField()
    image = models.ImageField(upload_to='recipec/', blank=True, null=True)

    class Meta:
        ordering = ["-pub_date"]


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
    obj = models.BooleanField(default=False)


class Purchases(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='user_shoping_list')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='recipe_shoping_list')


class Unit(models.Model):
    ingredients_unit = models.CharField(max_length=200)
    dimension = models.CharField(max_length=200)
