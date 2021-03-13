from django.contrib import admin
from .models import (
    Diet,
    Recipe,
    FavoritesRecipe,
    FollowUser,
    Purchases,
    RecipeIngridient,
    Ingredient)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'get_ingredients', 'get_diet', 'author')
    list_filter = ('pub_date')
    empty_value_display = '-пусто-'

    list_filter = ('title', 'author')
    search_fields = ('title', 'description')

    def get_diet(self, obj):
        return '\n'.join([p.title for p in obj.diets.all()])

    def get_ingredients(self, obj):
        return '\n'.join([p.title for p in obj.ingredients.all()])


class RecipeIngridientAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'recipe', 'amount')
    search_fields = ('ingredient',)
    list_filter = ('recipe',)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('title', 'dimension')
    search_fields = ('title',)


class DietAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    list_filter = ('title',)
    search_fields = ('title',)


class PurchasesAdmin(admin.ModelAdmin):
    model = Purchases
    list_display = ('user', 'recipe')
    list_filter = ('user',)


class FavoritesAdmin(admin.ModelAdmin):
    model = FavoritesRecipe
    list_display = ('user', 'following_recipe')
    list_filter = ('user',)


class FollowUserAdmin(admin.ModelAdmin):
    model = FavoritesRecipe
    list_display = ('user', 'author')
    list_filter = ('user',)


admin.site.register(FavoritesRecipe, FavoritesAdmin)
admin.site.register(FollowUser, FollowUserAdmin)
admin.site.register(Purchases, PurchasesAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(RecipeIngridient, RecipeIngridientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Diet, DietAdmin)
