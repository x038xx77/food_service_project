from django.contrib import admin
from .models import Recipe, Diet, FollowRecipe, FollowUser, Purchases, Unit


class RecipeAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "pub_date", "author", "diet", "ingredients")
    search_fields = ("title",)
    list_filter = ("pub_date",)
    empty_value_display = "-пусто-"


admin.site.register(Diet)
admin.site.register(FollowRecipe)
admin.site.register(FollowUser)
admin.site.register(Purchases)
admin.site.register(Unit)
admin.site.register(Recipe, RecipeAdmin)
