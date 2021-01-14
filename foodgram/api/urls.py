from django.urls import path
from . import views


urlpatterns = [
    # path('purchases/', views.Purchases.as_view()),
    # path('purchases/<int:purchase_id>', views.Purchases.as_view()),
    # path('subscriptions/', views.Subscriptions.as_view()),
    # path('subscriptions/<int:username_id>', views.Subscriptions.as_view()),
    # path('ingredients/', views.Ingredients.as_view()),
    path('favorites/', views.Favorites.as_view()),
    path('favorites/<int:recipe_id>', views.Favorites.as_view()),
    # path('ingredients/', views.Ingredients.as_view()),
]
