
from django.urls import path
from . import views

urlpatterns = [
    path('', views.RecipesView.as_view(), name='index'),
    path(
        '<str:username>/<int:recipe_id>/delete/',
        views.delete_recipe, name='delete_recipe'),
    path(
        'purcheses_download/',
        views.download_purcheses, name='purcheses_download'
        ),
    path('myfollow/', views.MyFollowView.as_view(), name='myfollow'),
    path('shop_list/', views.ShopListView.as_view(), name='shop_list'),
    path(
        'create_recipe/',
        views.CreateRecipeView.as_view(), name='create_recipe'),
    path(
        'favorite_list/',
        views.FavoritesView.as_view(), name='favorite_list'
        ),
    path(
        '<username>/', views.AuthorRecipeView.as_view(), name='author_recipe'),
    path(
        '<str:username>/<int:recipe_id>/',
        views.RecipeDetailView.as_view(), name='recipe'),
    path(
        '<str:username>/<int:recipe_id>/edit/',
        views.RecipeUpdateView.as_view(), name='recipe_edit'),
]
