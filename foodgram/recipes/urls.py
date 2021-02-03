from django.urls import path
from . import views

urlpatterns = [
    path('', views.RecipesView.as_view(), name='index'),
    path(
        '<username>/author_filter/',
        views.FilterAuthorDietView.as_view(), name='author_filter'),
    path(
        'follow_author_filter/',
        views.FilterFollowAuthorDietView.as_view(),
        name='follow_author_filter'),
    path(
        'purcheses_download/',
        views.purcheses_download, name='purcheses_download'
        ),
    path('myfollow/', views.MyFollowView.as_view(), name='myfollow'),
    path('shop_list/', views.shop_list, name='shop_list'),
    path('create_recipe/', views.create_recipe, name='create_recipe'),
    path(
        'favorite_list/',
        views.FavoritesView.as_view(), name='favorite_list'
        ),
    path(
        '<username>/', views.AuthorRecipeViev.as_view(), name='author_recipe'),
    path(
        '<str:username>/<int:recipe_id>/',
        views.recipe_view, name='recipe'),
    path(
        '<str:username>/<int:recipe_id>/edit/',
        views.recipe_edit, name='recipe_edit'),
    path(
        '<str:username>/<int:recipe_id>/delete/',
        views.recipe_delete, name='recipe_delete'),
]
