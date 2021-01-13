from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create_recipe/", views.new_recipe, name="new_recipe"),
    # path("formRecipe/", views.new_recipe, name="formRecipe"),
]