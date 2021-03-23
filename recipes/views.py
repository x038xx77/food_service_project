from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls.base import reverse_lazy
from .models import (
    Recipe, User,
    FollowUser, FavoritesRecipe, Purchases,
    RecipeIngridient)
from django.views.generic import (
    ListView,
    DetailView, CreateView,
    UpdateView, DeleteView)
from .forms import RecipeForm
from django.http import HttpResponse
from .utils import get_sort_list_tags
from django.db.models import Sum
from foodgram.settings import PAGINATE_BY
import csv
import logging
logger = logging.getLogger(__name__)


class RecipesView(ListView):
    """Список рецептов """
    template_name = 'index.html'
    paginate_by = PAGINATE_BY

    def get_queryset(self):
        queryset = Recipe.objects.all()
        sort_list = get_sort_list_tags(self.request)
        if sort_list:
            queryset = Recipe.objects.filter(
                diets__slug__in=sort_list).distinct()
        return queryset


class FavoritesView(ListView):
    """Список избранных рецептов."""
    model = FavoritesRecipe
    template_name = 'recipes/followrecipe_list.html'
    paginate_by = PAGINATE_BY

    def get_queryset(self):
        pk = FavoritesRecipe.objects.filter(
            user=self.request.user).values('following_recipe')
        queryset = Recipe.objects.filter(id__in=pk)
        sort_list = get_sort_list_tags(self.request)
        if sort_list:
            queryset = Recipe.objects.filter(
                id__in=pk, diets__slug__in=sort_list).distinct()
        return queryset


class RecipeDetailView(DetailView):
    """Детали рецепта."""
    model = Recipe
    template_name = 'recipes/single_page.html'
    pk_url_kwarg = 'recipe_id'


class AuthorRecipeView(ListView):
    """Список рецептов автора."""
    template_name = 'recipes/author_recipe_list.html'
    paginate_by = PAGINATE_BY

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        sort_list = get_sort_list_tags(self.request)
        queryset = Recipe.objects.filter(author=user)
        if sort_list:
            queryset = Recipe.objects.filter(
                diets__slug__in=sort_list, author=user).distinct()
        return queryset

    def get_context_data(self, **kwargs):
        context = super(
            AuthorRecipeView, self).get_context_data(**kwargs)
        context['author_recipe_name'] = get_object_or_404(
            User, username=self.kwargs.get('username'))
        return context


class MyFollowView(LoginRequiredMixin, ListView):
    """Подписка на автора рецепта."""
    model = FollowUser
    template_name = 'recipes/followuser_list.html'
    paginate_by = 3

    def get_queryset(self):
        queryset = FollowUser.objects.filter(user=self.request.user)
        return queryset


class CreateRecipeView(LoginRequiredMixin, CreateView):
    """Создание рецепта."""
    form_class = RecipeForm
    template_name = 'recipes/form_recipe.html'
    pk_url_kwarg = 'recipe_id'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdateRecipeView(LoginRequiredMixin, UpdateView):
    """Редактирование рецепта."""
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipes/form_recipe.html'
    pk_url_kwarg = 'recipe_id'
    success_url = reverse_lazy('index')


class DeleteRecipeView(DeleteView):
    """Удаление рецепта."""
    model = Recipe
    template_name = "recipes/recipe_congirm_delete.html"
    pk_url_kwarg = 'recipe_id'
    success_url = reverse_lazy('index')

    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(author=owner)


class ShopListView(ListView):
    """Список покупок."""
    model = Purchases
    template_name = 'shop_list.html'
    context_object_name = 'purchases'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            queryset = Recipe.objects.filter(
                shoping_list__user=self.request.user)
        else:
            try:
                queryset = Recipe.objects.filter(
                    pk__in=self.request.session['purchase'])
            except KeyError:
                queryset = []
        return queryset


def download_purchases(request):
    if request.user.is_authenticated:
        recipes_list = Recipe.objects.filter(shoping_list__user=request.user)
    else:
        recipes_list = Recipe.objects.filter(
            id__in=request.session.get('purchase'))
    list_ingredients = list(
        RecipeIngridient.objects.filter(recipe__id__in=recipes_list)
        .values('ingredient__title', 'ingredient__dimension')
        .annotate(total=Sum('amount'))
    )
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=Purchases_list.txt'
    writer = csv.writer(response)
    writer.writerow(['Наименование', '(единица измерения)', 'Кол-во'])
    for item in list_ingredients:
        title = item['ingredient__title']
        dimension = item['ingredient__dimension']
        amount = item['total']
        writer.writerow([title, ('({})').format(dimension), amount])
    return response


def page_not_found(request, exception):
    return render(
        request,
        'misc/404.html',
        {'path': request.path},
        status=404
    )


def server_error(request):
    return render(request, 'misc/500.html', status=500)
