from django.contrib import admin
from .models import (
    Diet,
    Recipe,
    FollowRecipe,
    FollowUser,
    Purchases,
    Tag,
    UnitIngredients
    )


class RecipeAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "pub_date", "author", "ingredients")
    list_filter = ("pub_date")
    empty_value_display = "-пусто-"

    list_filter = ('title', 'author')
    search_fields = ('title', 'description')


class UnitIngredientsAdmin(admin.ModelAdmin):
    list_display = ("id", "ingredients_unit", "dimension_unit")
    list_filter = ("pub_date")
    list_filter = ('ingredients_unit')
    search_fields = ("ingredients unit", "Dimension unit")


admin.site.register(FollowRecipe)
admin.site.register(FollowUser)
admin.site.register(Purchases)
admin.site.register(Diet)
admin.site.register(UnitIngredients)
admin.site.register(Tag)
admin.site.register(Recipe, RecipeAdmin)
