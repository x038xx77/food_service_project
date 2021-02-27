import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View

from recipes.models import (
    Recipe,
    FavoritesRecipe,
    FollowUser,
    User,
    Ingredient,
    Purchases)

JsonResponse_True = JsonResponse({'success': True})
JsonResponse_False = JsonResponse({'success': False}, status=400)


class Purchases_shop(LoginRequiredMixin, View):

    template_name = 'shopList.html'

    def post(self, request):
        reg = json.loads(request.body)
        recipe_id = reg.get('id', None)
        if recipe_id is not None:
            recipe = get_object_or_404(Recipe, id=recipe_id)
            if request.user.is_authenticated:
                obj, created = Purchases.objects.get_or_create(
                    user=request.user, recipe_id=recipe.id)
                return JsonResponse_True
            else:
                if 'purchase' not in request.session:
                    request.session['purchase'] = list()

                if recipe_id not in request.session['purchase']:
                    request.session['purchase'].append(recipe_id)
                    request.session.save()
                    return JsonResponse_True
            return JsonResponse({'success': False})
        return JsonResponse_False

    def delete(self, request, purchase_id):
        if request.user.is_authenticated:
            recipe = get_object_or_404(
                Purchases, recipe_id=purchase_id, user=request.user)
            recipe.delete()
        else:
            request.session['purchase'].remove(purchase_id)
            request.session.save()
        return JsonResponse_True


class Subscriptions(LoginRequiredMixin, View):

    def post(self, request):
        reg = json.loads(request.body)
        user_id = reg.get('id', None)
        if user_id is not None:
            author = get_object_or_404(User, pk=user_id)
            obj_exists = FollowUser.objects.get_or_create(
                user=request.user, author=author)
            if not obj_exists and author.id != request.user.id:
                obj, created = FollowUser.objects.create(
                    user=request.user, author=author)
                return JsonResponse_True
            return JsonResponse_True
        return JsonResponse_False

    def delete(self, request, username_id):
        recipe = get_object_or_404(
            FollowUser, author=username_id, user=request.user)
        recipe.delete()
        return JsonResponse_True


class Favorites(LoginRequiredMixin, View):

    def post(self, request):
        reg = json.loads(request.body)
        recipe_id = reg.get('id', None)
        if recipe_id is not None:
            recipe = get_object_or_404(Recipe, id=recipe_id)
            obj, created = FavoritesRecipe.objects.get_or_create(
                user=request.user, following_recipe_id=recipe.id)
            return JsonResponse_True
        return JsonResponse_False

    def delete(self, request, recipe_id):
        recipe = get_object_or_404(
            FavoritesRecipe, following_recipe=recipe_id, user=request.user)
        recipe.delete()
        return JsonResponse_True


def get_ingredients(request):
    list_unit_value = []
    part_product_name = request.GET.get('query', None)
    list_unit_value = Ingredient.objects.values(
        'title', 'dimension').filter(title__search=part_product_name)
    return JsonResponse(list(list_unit_value.values()), safe=False)
