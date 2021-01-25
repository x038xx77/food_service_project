import json # noqa
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.shortcuts import render

from recipes.models import (
    Recipe,
    FollowRecipe,
    FollowUser,
    User,
    Purchases,
    Unit
)


class Purchases_shop(View):

    template_name = "shopList.html"

    def post(self, request):
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
    # manager = request.GET["query"]
    dimension = []
    try:
        unit_dimension = Unit.objects.filter(
            ingredients_unit__icontains=part_product_name)
        dimension_1 = unit_dimension[0].dimension
        unit_title = part_product_name
        if dimension_1 is not None:
            dimension.append(dimension_1)
    except IndexError:
        pass
    if dimension[0] is not None:
        dimension = dimension[0]
    else:
        dimension = "шт"
    # unit_value = ([{
    #         "title": part_product_name,
    #         "dimension": dimension}])
    unit_value= [{"title": "гренадин", "dimension": "г"}]
    print("===", dimension)
    #return HttpResponse(unit_value)
    #return JsonResponse({"success": True})
    return render(request, 'formRecipe.html', {'dimension': dimension})
