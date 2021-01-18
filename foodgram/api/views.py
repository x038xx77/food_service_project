import json # noqa
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from api.serializers import UserSerializer

from recipes.models import (
    Recipe,
    FollowRecipe,
    FollowUser,
    User
)


class Purchases():
    """
    docstring
    """
    pass


class Subscriptions(LoginRequiredMixin, View):

    def post(self, request):
        reg = json.loads(request.body)
        user_id = reg.get("id", None)
        if user_id is not None:
            user_id = get_object_or_404(User, id=user_id)
            following, created = FollowUser.objects.get_or_create(
                user=request.user, following=user_id)
            if created:
                return JsonResponse({"success": True})
            return JsonResponse({"success": True})
        return JsonResponse({"success": False}, status=400)

    def delete(self, request, recipe_id):
        recipe = get_object_or_404(
            FollowRecipe, recipe=recipe_id, user=request.user)
        recipe.delete()
        return JsonResponse({"success": True})


class Favorites(LoginRequiredMixin, View):

    def post(self, request):
        reg = json.loads(request.body)
        recipe_id = reg.get("id", None)
        if recipe_id is not None:
            recipe = get_object_or_404(Recipe, id=recipe_id)
            obj, created = FollowRecipe.objects.get_or_create(
                user=request.user, following_recipe_id=recipe.id)
            if created:
                return JsonResponse({"success": True})
            return JsonResponse({"success": True})
        return JsonResponse({"success": False}, status=400)

    def delete(self, request, recipe_id):
        recipe = get_object_or_404(
            FollowRecipe, following_recipe=recipe_id, user=request.user)
        recipe.delete()
        return JsonResponse({"success": True})


class Ingredients(object):
    """
    docstring
    """
    pass


class UserFollowingViewSet(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = UserSerializer
    queryset = FollowUser.objects.all()

    # return JsonResponse({'status':status.HTTP_200_OK, 'data':{'user':serializer.data, 'following':following_data.data, 'followers':followers_data.data}, "message":"success"}) # noqa
