from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Diet(models.Model):
    title = models.CharField(max_length=7)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title


class Ingredients(models.Model):
    title = models.CharField(
        max_length=200, verbose_name='Название'
    )
    measurement_unit = models.CharField(
        max_length=20, verbose_name='Единица измерения'
    )


class Recipe(models.Model):
    text = models.TextField(
        'Текст рецепта', help_text="Please enter your Text...", default=None)
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


class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="follower")
    recipe = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="following")


class Purchases(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='user_shoping_list')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='recipe_shoping_list')
