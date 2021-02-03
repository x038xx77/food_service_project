from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Recipe, User, FollowUser, FollowRecipe, Diet, Purchases, Tag
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from .forms import RecipeForm
from django.http import HttpResponse
from .utils import (
    ingredient_arrey,
    tag_check, follow_id,
    is_tag, tag_create_chenge_template)
from .context_processors import get_tags

#from api.views import get_ingredients

import json # noqa
import csv


class Diets:
    def get_diet(self):
        return Diet.objects.all()


class RecipesView(Diets, ListView):
    """Список рецептов """

    paginate_by = 6

    def get_queryset(self):
        tag_check(self.request)
        queryset = Recipe.objects.filter(
            diets__in=get_tags(self)['url_list'])
        return queryset

    def get_context_data(self, **kwargs):
        context = super(
            RecipesView, self).get_context_data(**kwargs)
        quer = Recipe.objects.filter(
            diets__in=get_tags(self)['url_list'])
        context['follow_recipe_list'] = follow_id(quer)
        return context


class FilterAuthorDietView(Diets, ListView):
    # template_name = "author_filter.html"
    # context_object_name = 'author_filter'
    paginate_by = 6
    """Фильтр рациона автора"""
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        queryset = Recipe.objects.filter(
            diets__in=self.request.GET.getlist('diet'), author=user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(
            FilterAuthorDietView, self).get_context_data(**kwargs)
        context['author_filter_recipe'] = get_object_or_404(
            User, username=self.kwargs.get('username'))
        context['url_author_filter_recipe'] = self.request.get_full_path()
        return context


class FilterFollowAuthorDietView(Diets, ListView):
    # template_name = "filter.html"
    # context_object_name = 'follow_author_filter'
    paginate_by = 6
    """Фильтр рациона избранного"""
    def get_queryset(self):
        pk = FollowRecipe.objects.filter(
            user=self.request.user).values('following_recipe')
        queryset = Recipe.objects.filter(
            id__in=pk, diets__in=self.request.GET.getlist('diet'))
        return queryset


class FavoritesView(Diets, ListView):
    model = FollowRecipe
    queryset = FollowRecipe.objects.all()
    paginate_by = 6


def recipe_view(request, recipe_id, username):
    recipe = get_object_or_404(
        Recipe, pk=recipe_id, author__username=username)
    user = request.user
    if user.is_authenticated:
        following_recipe = FollowRecipe.objects.filter(
            user=user, following_recipe=recipe).exists()
    else:
        following_recipe = False
    return render(
        request,
        'singlePage.html',
        {
            'recipe': recipe, 'author': recipe.author,
            'following_recipe': following_recipe
            })


class AuthorRecipeViev(LoginRequiredMixin, Diets, ListView):

    template_name = "recipes/authorRecipe.html"
    # context_object_name = 'author_recipes'
    paginate_by = 6

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
       
        recepe_author = get_object_or_404(User, username=user)
        return recepe_author.recipes.all()

    def get_context_data(self, **kwargs):
        context = super(
            AuthorRecipeViev, self).get_context_data(**kwargs)
        context['author_recipe_name'] = get_object_or_404(
            User, username=self.kwargs.get('username'))
        follow_user = get_object_or_404(
            User, username=self.kwargs.get('username'))
        context['author_follow'] = FollowUser.objects.filter(
             author=follow_user)
        quer = Recipe.objects.filter(
            diets__in=get_tags(self)['url_list'])
        context['follow_recipe_list'] = follow_id(quer)
        return context


class MyFollowView(LoginRequiredMixin, ListView):
    model = FollowUser
    queryset = FollowUser.objects.all()
    paginate_by = 6


@login_required
def create_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, files=request.FILES or None)
        recipe_dict = request.POST.dict()
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            list_diet = tag_create_chenge_template(recipe, recipe_dict)
            if len(ingredient_arrey(
                request.POST.dict())) == 0 or len(
                    list_diet) == 0:
                recipe.delete()
                return render(
                    request, 'formRecipe.html', {
                        'form': form,
                        "error_ingredient":
                        "Ошибка введите ингредиенты и поставьте галочки"
                        })
            Recipe.objects.filter(
                author=recipe.author, id=recipe.id
                ).update(ingredients=ingredient_arrey(request.POST.dict()))
            return redirect('index')
    else:
        form = RecipeForm()
    return render(request, 'formRecipe.html', {'form': form})


@login_required
def recipe_edit(request, username, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id, author__username=username)
    if request.user != recipe.author:
        return redirect(
            'recipe', username=request.user.username, recipe_id=recipe_id)
    tag_breakfast = recipe.diets.filter(slug="breakfast")
    tag_lunch = recipe.diets.filter(slug="lunch")
    tag_dinner = recipe.diets.filter(slug="dinner")
    form = RecipeForm(
        request.POST or None, files=request.FILES or None, instance=recipe)
    recipe_dict = request.POST.dict()
    if form.is_valid():
        recipe.diets.clear()
        list_diet = tag_create_chenge_template(recipe, recipe_dict)
        if len(ingredient_arrey(
            request.POST.dict())) == 0 or len(
                list_diet) == 0:
            return render(
                request, 'formRecipe.html', {
                    'form': form,
                    "error_ingredient":
                    "Ошибка введите ингредиенты и поставьте галочки"
                    })
        form.save()
        Recipe.objects.filter(
            author=recipe.author, id=recipe.id
            ).update(ingredients=ingredient_arrey(request.POST.dict()))
        return redirect('index')
    return render(
        request, 'formChangeRecipe.html',
        {
            'form': form, 'recipe': recipe, 'tag_breakfast': tag_breakfast,
            'tag_dinner': tag_dinner, 'tag_lunch': tag_lunch
        })


@login_required
def recipe_delete(request, username, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id, author__username=username)
    if request.user != recipe.author:
        return redirect(
            'recipe', username=request.user.username, recipe_id=recipe_id)
    recipe.delete()
    return redirect('index')


def shop_list(request):
    count_purchase = Purchases.objects.all().count()
    print("================================", count_purchase)
    purchases = Purchases.objects.all()
    return render(
        request, 'shopList.html', {
            "purchases": purchases,
            "count_purchase": count_purchase})


def purcheses_download(request):
    items = {
        'nameIngredient': 'Яйцо',
        'valueIngredient': '5', 'unitsIngredient': 'ml'}
    response = HttpResponse(content_type='text/plain')
    response['Content-Type'] = 'text/plain'
    response[
        'Content-Disposition'
        ] = 'attachment; filename=DownloadedPurchases_list.txt'
    writer = csv.writer(response)
    writer.writerow(['nameingridient', 'valueingredient', 'unitingredient'])
    for key in items:
        print(items['nameIngredient'], items['valueIngredient'], items['unitsIngredient'])
        writer.writerow([
            items['nameIngredient'],
            items['valueIngredient'],
            items['unitsIngredient']])
    return response


def page_not_found(request, exception):
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )


def server_error(request):
    return render(request, "misc/500.html", status=500)
