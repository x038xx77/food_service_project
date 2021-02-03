import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View

from recipes.models import (
    Recipe,
    FollowRecipe,
    FollowUser,
    User,
    Purchases,
    UnitIngredients)


class Purchases_shop(LoginRequiredMixin, View):

    template_name = "shopList.html"

    def post(self, request):
        print(dir(request.GET))
        reg = json.loads(request.body)
        recipe_id = reg.get("id", None)
        if recipe_id is not None:
            recipe = get_object_or_404(Recipe, id=recipe_id)
            obj, created = Purchases.objects.get_or_create(
                user=request.user, recipe_id=recipe.id)
            if created:
                return JsonResponse({"success": True})
            return JsonResponse({"success": True})
        return JsonResponse({"success": False}, status=400)

    def delete(self, request, purchase_id):
        recipe = get_object_or_404(
            Purchases, recipe_id=purchase_id, user=request.user)
        recipe.delete()
        return JsonResponse({"success": True})


class Subscriptions(LoginRequiredMixin, View):

    def post(self, request):
        reg = json.loads(request.body)
        user_id = reg.get("id", None)
        if user_id is not None:
            username = User.objects.get(pk=user_id)
            author = get_object_or_404(User, username=username)
            obj_exists = FollowUser.objects.filter(
                user=request.user, author=author).exists()
            if not obj_exists and author.id != request.user.id:
                created = FollowUser.objects.create(
                    user=request.user, author=author)
                if created:
                    return JsonResponse({"success": True})
                return JsonResponse({"success": True})
            return JsonResponse({"success": False}, status=400)

    def delete(self, request, username_id):
        recipe = get_object_or_404(
            FollowUser, author=username_id, user=request.user)
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


def get_ingredients(request):
    part_product_name = request.GET.get('query', None)
    unit_value = {}
    list_unit_value = []
    try:
        unit_dimension = UnitIngredients.objects.filter(
            ingredients_unit__icontains=part_product_name)
        j = 1
        for i in unit_dimension:
            unit_value['nameIngredient_unit_' + str(j)] = i.ingredients_unit
            unit_value['valueIngredient_unit_' + str(j)] = i.dimension_unit
            j += 1
        update = []
        items = list(unit_value.items())
        for i in range(len(items) // 2):
            _tmp = items[2 * i:2 * (i + 1)]
            update.append(_tmp)
        new_list_key = ["title", "dimension"]
        old_arrey = update
        list_unit_value = []
        for i in old_arrey:
            new_dict = {}
            t = 0
            for key, value in dict(i).items():
                new_dict[new_list_key[t]] = value
                t += 1
            list_unit_value.append(new_dict)
    except IndexError:
        pass
    return JsonResponse(
        list_unit_value, safe=False)
