from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls.base import reverse_lazy
from .models import (
    Recipe,
    FollowUser, FollowRecipe, Diet, Purchases,
    RecipeIngridient,
    Ingredient)
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    ListView,
    DetailView, CreateView,
    UpdateView, DeleteView)
from .forms import RecipeForm
from django.http import HttpResponse
from .utils import (
    tag_create_change_template,
    ingredient_array,
    print_list_purchases)

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

        queryset = Recipe.objects.filter(
            diets__in=self.request.GET.getlist('diet', None))
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
        url_param_breakfast = []
        url_param_lunch = []
        url_param_dinner = []
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
            url_param_breakfast.append('diet=1')
        else:
            is_breakfast = False
            url_param_breakfast = []
        if tag_lunch.filter(published=True).exists():
            url_param_lunch.append('diet=2')
            is_lunch = True
        else:
            is_lunch = False
            url_param_lunch = []
        if tag_dinner.filter(published=True).exists():
            is_dinner = True
            url_param_dinner.append('diet=3')
        else:
            is_dinner = False
            url_param_dinner = []
        context['tag_breakfast'] = is_breakfast
        context['tag_lunch'] = is_lunch
        context['tag_dinner'] = is_dinner
        context['url_breakfast'] = url_breakfast
        context['url_lunch'] = url_lunch
        context['url_dinner'] = url_dinner
        context['url_param_breakfast'] = url_param_breakfast
        context['url_param_lunch'] = url_param_lunch
        context['url_param_dinner'] = url_param_dinner
        context['form'] = form
        return context


class FavoritesView(Diets, ListView):
    model = FollowRecipe
    paginate_by = 6


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = "singlePage.html"
    pk_url_kwarg = 'recipe_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipe = get_object_or_404(
            Recipe, pk=self.kwargs['recipe_id'],
            author__username=self.kwargs['username'])
        recipe_ingredient = RecipeIngridient.objects.filter(recipe=recipe)
        following_recipe = FollowRecipe.objects.filter(
            following_recipe=recipe).exists()
        context['following_recipe'] = following_recipe
        context['recipe_ingredient'] = recipe_ingredient
        return context


class AuthorRecipeView(Diets, ListView):

    template_name = "recipes/authorRecipe.html"
    paginate_by = 6


class MyFollowView(LoginRequiredMixin, ListView):
    model = FollowUser
    queryset = FollowUser.objects.all()
    paginate_by = 6


class CreateRecipeView(LoginRequiredMixin, CreateView):
    form_class = RecipeForm
    template_name = 'formRecipe.html'
    pk_url_kwarg = 'recipe_id'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.save
        self.object = form.save()
        recipe_dict = self.request.POST.dict()
        for ingredient in ingredient_array(self.request.POST.dict()):
            ingredient_recipe = get_object_or_404(
                Ingredient, title=ingredient['nameIngredient'])
            RecipeIngridient.objects.get_or_create(
                recipe=obj, ingredient=ingredient_recipe,
                amount=ingredient['valueIngredient']
                )
        list_diet = tag_create_change_template(obj, recipe_dict)
        if len(ingredient_array(
                self.request.POST.dict())) == 0 or len(list_diet) == 0:
            obj.delete()
            return render(
                self.request, 'formRecipe.html', {
                    'form': form,
                    "error_ingredient":
                    "Ошибка введите ингредиенты и поставьте галочки"
                        })
        return super().form_valid(form)


class RecipeUpdateView(LoginRequiredMixin, UpdateView):

    model = Recipe
    form_class = RecipeForm
    template_name = 'formChangeRecipe.html'
    pk_url_kwarg = 'recipe_id'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user

        self.object = form.save()
        recipe_dict = self.request.POST.dict()
        if form.is_valid():
            obj.diets.clear()
            list_diet = tag_create_change_template(obj, recipe_dict)
            if len(ingredient_array(
                self.request.POST.dict())) == 0 or len(
                    list_diet) == 0:
                return render(
                    self.request, 'formRecipe.html', {
                        'form': form,
                        "error_ingredient":
                        "Ошибка введите ингредиенты и поставьте галочки"
                        })
        obj.save
        for ingredient in ingredient_array(self.request.POST.dict()):
            ingredient_recipe = get_object_or_404(
                Ingredient, title=ingredient['nameIngredient'])
            RecipeIngridient.objects.get_or_create(
                recipe=obj, ingredient=ingredient_recipe,
                amount=ingredient['valueIngredient']
                )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(RecipeUpdateView, self).get_context_data(**kwargs)
        recipe = get_object_or_404(
            Recipe, pk=self.kwargs['recipe_id'],
            author__username=self.kwargs['username'])
        ingredient_recipe = RecipeIngridient.objects.filter(recipe=recipe)
        tag_breakfast = recipe.diets.filter(slug="breakfast")
        tag_lunch = recipe.diets.filter(slug="lunch")
        tag_dinner = recipe.diets.filter(slug="dinner")
        context['tag_breakfast'] = tag_breakfast
        context['tag_lunch'] = tag_lunch
        context['tag_dinner'] = tag_dinner
        context['ingredient_recipe'] = ingredient_recipe
        return context


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
