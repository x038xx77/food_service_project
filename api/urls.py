
from django.urls import path
from . import views


urlpatterns = [
    path('purchases', views.Purchases_shop.as_view(), name='shop_list'),
    path(
        'purchases/<int:purchase_id>',
        views.Purchases_shop.as_view()),
    path('subscriptions', views.Subscriptions.as_view(), name='myfollow'),
    path('subscriptions/<int:username_id>', views.Subscriptions.as_view()),
    path('favorites', views.Favorites.as_view(), name='favorite_list'),
    path('favorites/<int:recipe_id>', views.Favorites.as_view()),
    path('ingredients', views.GetIngredients.as_view(), name='ingredients'),
]
