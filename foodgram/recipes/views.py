from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls.base import reverse_lazy
from .models import (
    Recipe, User,
    FollowUser, FavoritesRecipe, Purchases,
    RecipeIngridient)
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    ListView,
    DetailView, CreateView,
    UpdateView)
from .forms import RecipeForm
from django.http import HttpResponse
import csv
from collections import defaultdict
from foodgram.settings import PAGINATE_BY
import logging
logger = logging.getLogger(__name__)


class RecipesView(ListView):
    """Список рецептов """
    paginate_by = PAGINATE_BY

    def get_queryset(self):
        queryset = Recipe.objects.all()
        sort_list = self.request.GET.getlist('tag', None)
        if sort_list:
            queryset = Recipe.objects.filter(diets__slug__in=sort_list)
        return queryset


class FavoritesView(ListView):
    model = FavoritesRecipe

    def get_queryset(self):
        pk = FavoritesRecipe.objects.filter(
            user=self.request.user).values('following_recipe')
        queryset = Recipe.objects.filter(
            id__in=pk, diets__slug__in=self.request.GET.getlist('tag', None))
        return queryset


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'singlePage.html'
    pk_url_kwarg = 'recipe_id'


class AuthorRecipeView(ListView):

    template_name = 'recipes/authorRecipe.html'

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        queryset = Recipe.objects.filter(
            diets__slug__in=self.request.GET.getlist('tag', None), author=user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(
            AuthorRecipeView, self).get_context_data(**kwargs)
        context['author_recipe_name'] = get_object_or_404(
            User, username=self.kwargs.get('username'))
        return context


class MyFollowView(LoginRequiredMixin, ListView):
    model = FollowUser
    template_name = 'recipes/followuser_list.html'
    paginate_by = 3

    def get_queryset(self):
        queryset = FollowUser.objects.filter(user=self.request.user)
        return queryset


class CreateRecipeView(LoginRequiredMixin, CreateView):

    form_class = RecipeForm
    template_name = 'recipes/formRecipe.html'
    pk_url_kwarg = 'recipe_id'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdateRecipeView(LoginRequiredMixin, UpdateView):

    model = Recipe
    form_class = RecipeForm
    template_name = 'recipes/formRecipe.html'
    pk_url_kwarg = 'recipe_id'
    success_url = reverse_lazy('index')


class ShopListView(ListView):
    model = Purchases
    template_name = 'shopList.html'
    context_object_name = 'purchases'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            queryset = Purchases.objects.filter(user=self.request.user)
        else:
            try:
                queryset = Recipe.objects.filter(
                    pk__in=self.request.session['purchase'])
            except Exception as e:
                logger.error(str(e))
                queryset = []
        return queryset


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

    dict_set_ingedient = defaultdict(list)
    for name_value_ingredient, unit_ingredient in list_ingredient:
        dict_set_ingedient[name_value_ingredient].append(int(unit_ingredient))

    response = HttpResponse(content_type='text/plain')
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
        'misc/404.html',
        {'path': request.path},
        status=404
    )


def server_error(request):
    return render(request, 'misc/500.html', status=500)
