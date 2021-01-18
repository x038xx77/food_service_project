from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from api.views import UserFollowingViewSet

router_v1 = DefaultRouter()
router_v1.register('subscriptions', UserFollowingViewSet)


urlpatterns = [
    #path('v1/', include(router_v1.urls)),
    #path('v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    #path('v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('purchases/', views.Purchases.as_view()),
    # path('purchases/<int:purchase_id>', views.Purchases.as_view()),
    path('subscriptions/', views.Subscriptions.as_view()),
    path('subscriptions/<int:username_id>', views.Subscriptions.as_view()),
    # path('ingredients/', views.Ingredients.as_view()),
    path('favorites', views.Favorites.as_view(), name="favorite_list"),
    path('favorites/<int:recipe_id>', views.Favorites.as_view()),
    # path('ingredients/', views.Ingredients.as_view()),
]
