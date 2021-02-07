from django.contrib import admin
from .models import (
    Diet,
    Recipe,
    FollowRecipe,
    FollowUser,
    Purchases,
    RecipeIngridient,
    Ingredient
    )


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'get_ingredients', 'get_diet', 'author')
    list_filter = ('pub_date')
    empty_value_display = '-пусто-'

    list_filter = ('title', 'author')
    search_fields = ('title', 'description')

    def get_diet(self, obj):
        return "\n".join([p.title for p in obj.diets.all()])

    def get_ingredients(self, obj):
        return "\n".join([p.title for p in obj.ingredients.all()])


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


admin.site.register(FollowRecipe)
admin.site.register(FollowUser)
admin.site.register(Purchases)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(RecipeIngridient, RecipeIngridientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Diet, DietAdmin)
