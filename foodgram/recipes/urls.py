from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create_recipe/", views.create_recipe, name="create_recipe"),
    path("myfollow/", views.myfollow, name="myfollow"),
    path('<username>/', views.author_recipe, name='author_recipe'),
    path('<str:username>/<int:recipe_id>/', views.recipe_view, name='recipe'),
    path(
        '<str:username>/<int:recipe_id>/edit/',
        views.recipe_edit, name='recipe_edit'),
]
