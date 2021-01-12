from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # path("formRecipe/", views.new_recipe, name="formRecipe"),
]