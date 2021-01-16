from django.contrib import admin
from .models import Recipe, Diet, Ingredient, RecipeIngridient, FollowRecipe # noqa


class RecipeAdmin(admin.ModelAdmin):
    list_display = ("title", "pub_date", "author", "diet")
    search_fields = ("title",)
    list_filter = ("pub_date",)
    empty_value_display = "-пусто-"


admin.site.register(Diet)
admin.site.register(Ingredient)
admin.site.register(RecipeIngridient)
admin.site.register(FollowRecipe)
admin.site.register(Recipe, RecipeAdmin)
