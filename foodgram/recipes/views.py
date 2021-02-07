from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import (
    Recipe, User,
    FollowUser, FollowRecipe, Diet, Purchases, Ingredient)
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from .forms import RecipeForm
from django.http import HttpResponse

import json # noqa
import csv
from .forms import MyForm

class Diets:
    def get_diet(self):
        return Diet.objects.all()


class RecipesView(Diets, ListView):
    """Список рецептов """

    paginate_by = 6

    def get_queryset(self):

        queryset = Recipe.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super(
            RecipesView, self).get_context_data(**kwargs)
        form = MyForm(self.request.GET or None)
        print("========")
        tag_lunch = Diet.objects.filter(slug='lunch')
        tag_dinner = Diet.objects.filter(slug='dinner')
        tag_breakfast = Diet.objects.filter(slug='breakfast')
        url_breakfast = 'breakfast=on'
        url_lunch = 'lunch=on'
        url_dinner = 'dinner=on'
        breakfast = self.request.GET.getlist('breakfast')
        lunch = self.request.GET.getlist('lunch')
        dinner = self.request.GET.getlist('dinner')
        diet = self.request.GET.getlist('diet')
        print("getlist", breakfast, lunch, dinner, diet)
    
        try:
            for i in breakfast:
                if i == 'on':
                    if tag_breakfast.filter(published=True).exists():
                        tag_breakfast.update(published=False)
                    else:
                        tag_breakfast.update(published=True)
            for i in lunch:
                if i == 'on':
                    if tag_lunch.filter(published=True).exists():
                        tag_lunch.update(published=False)
                    else:
                        tag_lunch.update(published=True)
            for i in dinner:
                if i == 'on':
                    if tag_dinner.filter(published=True).exists():
                        tag_dinner.update(published=False)
                    else:
                        tag_dinner.update(published=True)
        except IndexError:
            pass
        if tag_breakfast.filter(published=True).exists():
            is_breakfast = True
        else:
            is_breakfast = False
        if tag_lunch.filter(published=True).exists():
            is_lunch = True
        else:
            is_lunch = False
        if tag_dinner.filter(published=True).exists():
            is_dinner = True
        else:
            is_dinner = False
        url_param = []
        try:
            # if tag_breakfast.filter(published=False).exists():
            #     url_param = ['diet=1']
            # if tag_lunch.filter(published=False).exists():
            #     url_param = ['diet=2']
            # if tag_dinner.filter(published=False).exists():
            #     url_param = ['diet=3']
            if tag_breakfast.filter(published=True).exists() and tag_lunch.filter(published=True).exists():
                url_param = ['diet=1&diet=2']
            if tag_breakfast.filter(published=True).exists() and tag_dinner.filter(published=True).exists():
                url_param = ['diet=1&diet=3']
            if tag_lunch.filter(published=True).exists() and tag_dinner.filter(published=True).exists():
                url_param = ['diet=2&diet=3']
            if tag_breakfast.filter(published=True).exists() and tag_lunch.filter(published=True).exists() and tag_dinner.filter(published=True).exists():
                url_param = ['diet=1&diet=2&diet=3']
        except IndexError:
            pass

        context['tag_breakfast'] = is_breakfast
        context['tag_lunch'] = is_lunch
        context['tag_dinner'] = is_dinner
        context['url_breakfast'] = url_breakfast
        context['url_lunch'] = url_lunch
        context['url_dinner'] = url_dinner
        context['url_param'] = url_param
        context['form'] = form
        return context

class FavoritesView(Diets, ListView):
    model = FollowRecipe
    paginate_by = 6


def recipe_view(request, recipe_id, username):
    recipe = get_object_or_404(
        Recipe, pk=recipe_id, author__username=username)
    user = request.user
    author_follow = FollowUser.objects.filter(
             author=recipe.author)
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
            'following_recipe': following_recipe,
            'author_follow': author_follow
            })


class AuthorRecipeViev(Diets, ListView):

    template_name = "recipes/authorRecipe.html"
    # context_object_name = 'author_recipes'
    paginate_by = 6



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
    purchases = Purchases.objects.all()
    return render(
        request, 'shopList.html', {
            "purchases": purchases,
            "count_purchase": count_purchase})


@login_required
def purcheses_download(request):
    purchases = Purchases.objects.all()
    list_all_purchases = []
    for i in purchases:
        list_all_purchases += i.recipe.ingredients
    response = HttpResponse(content_type='text/plain')
    response['Content-Type'] = 'text/plain'
    response[
        'Content-Disposition'
        ] = 'attachment; filename=DownloadedPurchases_list.txt'
    writer = csv.writer(response)
    writer.writerow(['Наименование', 'Кол-во'])
    for key, value in print_list_purchases(list_all_purchases).items():
        writer.writerow([str(key) + str(value)])
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
