import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.db.models import F
from recipes.models import (
    Recipe,
    FavoritesRecipe,
    FollowUser,
    User,
    Ingredient,
    Purchases)
import logging
logger = logging.getLogger(__name__)

JsonResponseTrue = JsonResponse({'success': True})
JsonResponseFalse = JsonResponse({'success': False}, status=400)


class Purchases_shop(View):
    template_name = 'shop_list.html'

    def post(self, request):
        reg = json.loads(request.body)
        recipe_id = reg.get('id')
        if not recipe_id:
            return JsonResponseFalse

        recipe = get_object_or_404(Recipe, id=recipe_id)
        if request.user.is_authenticated:
            obj, created = Purchases.objects.get_or_create(
                user=request.user, recipe_id=recipe.id)
            return JsonResponseTrue

        if 'purchase' not in request.session:
            request.session['purchase'] = []
        if recipe_id not in request.session['purchase']:
            request.session['purchase'].append(recipe_id)
            request.session.save()
            return JsonResponseTrue

    def delete(self, request, purchase_id):
        if request.user.is_authenticated:
            recipe = get_object_or_404(
                Purchases, recipe_id=purchase_id, user=request.user)
            recipe.delete()
        else:
            request.session['purchase'].remove(str(purchase_id))
            request.session.save()
        return JsonResponseTrue


class Subscriptions(LoginRequiredMixin, View):

    def post(self, request):
        reg = json.loads(request.body)
        user_id = reg.get('id')
        if not user_id:
            return JsonResponseFalse

        author = get_object_or_404(User, pk=user_id)
        obj, created = FollowUser.objects.get_or_create(
            user=request.user, author=author)
        return JsonResponseTrue

    def delete(self, request, username_id):
        recipe = get_object_or_404(
            FollowUser, author=username_id, user=request.user)
        recipe.delete()
        return JsonResponseTrue


class Favorites(LoginRequiredMixin, View):

    def post(self, request):
        reg = json.loads(request.body)
        recipe_id = reg.get('id')
        if not recipe_id:
            return JsonResponseFalse

        recipe = get_object_or_404(Recipe, id=recipe_id)
        obj, created = FavoritesRecipe.objects.get_or_create(
            user=request.user, following_recipe_id=recipe.id)
        return JsonResponseTrue

    def delete(self, request, recipe_id):
        recipe = get_object_or_404(
            FavoritesRecipe, following_recipe=recipe_id, user=request.user)
        recipe.delete()
        return JsonResponseTrue


class GetIngredients(LoginRequiredMixin, View):

    def get(self, request):
        part_product_name = request.GET['query'].lower()
        list_unit_value = list(Ingredient.objects.filter(
            title__startswith=part_product_name)
            .annotate(name=F('title'), unit=F('dimension'))
            .values('title', 'dimension'))
        return JsonResponse(list_unit_value, safe=False)
