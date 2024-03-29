from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

User = get_user_model()


class Recipe(models.Model):
    title = models.TextField(
        'Название рецепта',
        default=None)
    ingredients = models.ManyToManyField(
        'Ingredient', blank=True, through='RecipeIngridient',
        verbose_name='Ингредиенты')
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='recipes',
        verbose_name='автор рецепта')
    diets = models.ManyToManyField(
        'Diet', blank=True, related_name='recipe_set', verbose_name='рацион')
    description = models.TextField(verbose_name='описание рецепта')
    cooking_time = models.IntegerField(
        validators=[MinValueValidator(1)], verbose_name='время приготовления')
    image = models.ImageField(
        upload_to='recipes/')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class Ingredient(models.Model):
    title = models.CharField(
        unique=True, max_length=300, verbose_name='название')
    dimension = models.CharField(max_length=300, verbose_name='размерность')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Ингредиенты'


class RecipeIngridient(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient',
        verbose_name='ингредиент'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredient_recipes',
        verbose_name='рецепт ингредиента'
    )
    amount = models.IntegerField(
        validators=[MinValueValidator(1)], verbose_name='значение')

    def __str__(self):
        return self.recipe.title

    class Meta:
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецепта'


class Diet(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)
    checkbox_style = models.CharField(max_length=50)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Рацион'


class FollowUser(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='follower')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'], name='unique_subscription'),
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'


class FavoritesRecipe(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='favorites')
    following_recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='favorites')

    class Meta:
        verbose_name_plural = 'Избранные рецепты'


class Purchases(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='shoping_list')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='shoping_list')

    class Meta:
        verbose_name_plural = 'Покупки'
