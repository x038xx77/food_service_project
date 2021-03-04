from django.shortcuts import render
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
    UpdateView, DeleteView)
from .forms import RecipeForm
from django.http import HttpResponse
from .utils import get_sort_list_tags
from django.db.models import Sum
from foodgram.settings import PAGINATE_BY
import logging
logger = logging.getLogger(__name__)


class RecipesView(ListView):
    """Список рецептов """
    paginate_by = PAGINATE_BY

    def get_queryset(self):
        queryset = Recipe.objects.all()
        sort_list = get_sort_list_tags(self.request)
        if sort_list:
            queryset = Recipe.objects.filter(diets__slug__in=sort_list)
        return queryset


class FavoritesView(ListView):
    """Список избранных рецептов."""
    model = FavoritesRecipe
    paginate_by = PAGINATE_BY

    def get_queryset(self):
        pk = FavoritesRecipe.objects.filter(
            user=self.request.user).values('following_recipe')
        queryset = Recipe.objects.filter(
                id__in=pk)
        sort_list = get_sort_list_tags(self.request)
        if sort_list:
            queryset = Recipe.objects.filter(
                id__in=pk, diets__slug__in=sort_list)
        return queryset


class RecipeDetailView(DetailView):
    """Детали рецепта."""
    model = Recipe
    template_name = 'recipes/singlePage.html'
    pk_url_kwarg = 'recipe_id'


class AuthorRecipeView(ListView):
    """Список рецептов автора."""
    template_name = 'recipes/authorRecipe.html'
    paginate_by = PAGINATE_BY

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        sort_list = get_sort_list_tags(self.request)
        queryset = Recipe.objects.filter(author=user)
        if sort_list:
            queryset = Recipe.objects.filter(
                diets__slug__in=sort_list, author=user)
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
    template_name = 'recipes/formRecipe.html'
    pk_url_kwarg = 'recipe_id'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdateRecipeView(LoginRequiredMixin, UpdateView):
    """Редактирование рецепта."""
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipes/formRecipe.html'
    pk_url_kwarg = 'recipe_id'
    success_url = reverse_lazy('index')


class DeleteRecipeView(DeleteView):
    """Удаление рецепта."""
    model = Recipe
    template_name = "recipes/recipe_congirm_delete.html"
    pk_url_kwarg = 'recipe_id'
    success_url = reverse_lazy("index")

    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(author=owner)


class ShopListView(ListView):
    """Список покупок."""
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
def download_purchases(request):

    recipes_list = Recipe.objects.filter(shoping_list__user=request.user)
    list_ingredients = (
        RecipeIngridient.objects.filter(recipe__id__in=recipes_list)
        .values('ingredient__title', 'ingredient__dimension')
        .annotate(total=Sum('amount'))
    )
    context = ''
    for item in list_ingredients:
        row = ' '.join(str(value) for value in item.values())
        context += row + '\n'

    response = HttpResponse(context, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=Purchases_list.txt'
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
