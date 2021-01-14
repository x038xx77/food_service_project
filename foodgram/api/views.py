import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View

from recipes.models import (
    Recipe,
    FollowRecipe,
)


class Purchases():
    """
    docstring
    """
    pass


class Subscriptions():
    """
    docstring
    """
    pass


class Favorites(LoginRequiredMixin, View):
    def post(self, request):
        reg = json.loads(request.body)
        recipe_id = reg.get("id", None)
        if recipe_id is not None:
            recipe = get_object_or_404(Recipe, id=recipe_id)
            obj, created = FollowRecipe.objects.get_or_create(
                user=request.user, recipe=recipe)
            if created:
                return JsonResponse({"success": True})
            return JsonResponse({"success": True})
        return JsonResponse({"success": False}, status=400)

    def delete(self, request, recipe_id):
        recipe = get_object_or_404(
            FollowRecipe, recipe=recipe_id, user=request.user)
        recipe.delete()
        return JsonResponse({"success": True})


class Ingredients(object):
    """
    docstring
    """
    pass
