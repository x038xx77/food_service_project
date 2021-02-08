from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls.base import reverse_lazy
from .models import (
    Recipe, User,
    FollowUser, FollowRecipe, Diet, Purchases,
    RecipeIngridient,
    Ingredient)
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    ListView,
    DetailView, CreateView,
    UpdateView)
from .forms import RecipeForm
from django.http import HttpResponse
from .utils import (
    tag_create_change_template,
    get_ingredients_from,
    is_empty_ingredients,
    follow_id)
import json # noqa
import csv


class Diets:
    def get_diet(self):
        return Diet.objects.all()


class RecipesView(Diets, ListView):
    """Список рецептов """

    def get_queryset(self):
        sort_list = self.request.GET.getlist('diet', None)
        queryset = Recipe.objects.filter(
            diets__in=sort_list)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(
            RecipesView, self).get_context_data(**kwargs)
        quer = Recipe.objects.filter(
            diets__in=self.request.GET.getlist('diet', None))
        context['follow_recipe_list'] = follow_id(quer)
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
        return context


class FavoritesView(Diets, ListView):
    model = FollowRecipe

    def get_queryset(self):
        pk = FollowRecipe.objects.filter(
            user=self.request.user).values('following_recipe')
        queryset = Recipe.objects.filter(
            id__in=pk, diets__in=self.request.GET.getlist('diet', None))
        return queryset


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = "singlePage.html"
    pk_url_kwarg = 'recipe_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipe = get_object_or_404(
            Recipe, pk=self.kwargs['recipe_id'],
            author__username=self.kwargs['username'])
        author_follow = FollowUser.objects.filter(
             author=recipe.author)
        recipe_ingredient = RecipeIngridient.objects.filter(recipe=recipe)
        following_recipe = FollowRecipe.objects.filter(
            following_recipe=recipe).exists()
        context['following_recipe'] = following_recipe
        context['recipe_ingredient'] = recipe_ingredient
        context['recipe'] = recipe
        context['author'] = recipe.author
        context['author_follow'] = author_follow
        return context


class AuthorRecipeView(Diets, ListView):

    template_name = "recipes/authorRecipe.html"

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        queryset = Recipe.objects.filter(
            diets__in=self.request.GET.getlist('diet', None), author=user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(
            AuthorRecipeView, self).get_context_data(**kwargs)
        context['author_recipe_name'] = get_object_or_404(
            User, username=self.kwargs.get('username'))
        follow_user = get_object_or_404(
            User, username=self.kwargs.get('username'))
        context['author_follow'] = FollowUser.objects.filter(
             author=follow_user)
        quer = Recipe.objects.filter(
            diets__in=self.request.GET.getlist('diet', None))
        context['follow_recipe_list'] = follow_id(quer)
        return context


class MyFollowView(LoginRequiredMixin, ListView):
    model = FollowUser
    queryset = FollowUser.objects.all()


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
        for nameIngr, valueIngr, unitsIngr in get_ingredients_from(self.request.POST.dict()):  # noqa
            ingredient_recipe = get_object_or_404(
                Ingredient, title=nameIngr)
            RecipeIngridient.objects.get_or_create(
                recipe=obj, ingredient=ingredient_recipe,
                amount=valueIngr
                )
        list_diet = tag_create_change_template(obj, recipe_dict)
        if is_empty_ingredients(get_ingredients_from(
                self.request.POST.dict())) or len(list_diet) == 0:
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
            data = self.request.POST.dict()
            if is_empty_ingredients(
                get_ingredients_from(data)) or len(list_diet) == 0: # noqa
                return render(
                    self.request, 'formRecipe.html', {
                        'form': form,
                        "error_ingredient":
                        "Ошибка введите ингредиенты и поставьте галочки"
                        })
        obj.save
        for nameIngr, valueIngr, unitsIngr in get_ingredients_from(self.request.POST.dict()):  # noqa
            ingredient_recipe = get_object_or_404(
                Ingredient, title=nameIngr)
            RecipeIngridient.objects.get_or_create(
                recipe=obj, ingredient=ingredient_recipe,
                amount=valueIngr
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


class ShopListView(ListView):
    model = Purchases
    template_name = 'shopList.html'
    context_object_name = 'purchases'


@login_required
def download_purcheses(request):
    purchases = Purchases.objects.all()
    list_name_unit = []
    list_value = []
    for obj in purchases:
        recipe_ingredients = RecipeIngridient.objects.filter(recipe=obj.recipe)
        for item in recipe_ingredients:
            list_name_unit.append(
                ('{} ({}) - ').format(
                    item.ingredient, item.ingredient.dimension))
            list_value.append(item.amount)
    list_ingredient = list(zip(list_name_unit, list_value))
    dict_set_ingedient = {}
    for name_value_ingredient, unit_ingredient in list_ingredient:
        dict_set_ingedient.setdefault(
            name_value_ingredient, []).append(int(unit_ingredient))
    response = HttpResponse(content_type='text/plain')
    response['Content-Type'] = 'text/plain'
    response['Content-Disposition'] = 'attachment; filename=Purchases_list.txt'
    writer = csv.writer(response)
    writer.writerow(['Наименование (единица измерения)', 'Кол-во'])
    for name_value_ingredient, unit_ingredient in dict_set_ingedient.items():
        writer.writerow(
            [str(name_value_ingredient), str(sum(unit_ingredient))])
    return response


@login_required
def delete_recipe(request, username, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id, author__username=username)
    if request.user != recipe.author:
        return redirect(
            'recipe', username=request.user.username, recipe_id=recipe_id)
    recipe.delete()
    return redirect('index')


def page_not_found(request, exception):
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )


def server_error(request):
    return render(request, "misc/500.html", status=500)
