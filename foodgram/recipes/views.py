from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View
from .models import Recipe, User, FollowUser, FollowRecipe, Diet, Purchases
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from .forms import RecipeForm
from .utils import ingredient_arrey
from django.contrib.auth.mixins import LoginRequiredMixin
import json # noqa


class Diets:
    def get_diet(self):
        return Diet.objects.all()


class RecipesView(Diets, ListView):
    """Список """
    model = Recipe
    queryset = Recipe.objects.all()
    paginate_by = 6


class FilterDietView(Diets, ListView):
    """Фильтр diet"""
    def get_queryset(self):
        queryset = Recipe.objects.filter(
            diets__in=self.request.GET.getlist("diet"))
        return queryset


class FavoritesView(Diets, ListView):
    model = FollowRecipe
    queryset = FollowRecipe.objects.all()
    paginate_by = 5


def page_not_found(request, exception):
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )


def server_error(request):
    return render(request, "misc/500.html", status=500)


def recipe_view(request, recipe_id, username):
    recipe = get_object_or_404(
        Recipe, pk=recipe_id, author__username=username)
    user = request.user
    if user.is_authenticated:
        following_recipe = FollowRecipe.objects.filter(
            user = user, # noqa
            following_recipe = recipe).exists() # noqa
    else:
        following_recipe = False

    t={"nameIngredient_1": "\u041c\u043e\u043b\u043e\u043a\u043e", "valueIngredient_1": "3", "unitsIngredient_1": "y.e1", "nameIngredient_2": "\u042f\u0439\u0446\u043e", "valueIngredient_2": "3", "unitsIngredient_2": "y.e2", "nameIngredient_3": "\u0440\u0438\u0441", "valueIngredient_3": "2", "unitsIngredient_3": "y.e3"}
    count= len(t)/3
    return render(
        request,
        'singlePage.html',
        {
            'recipe': recipe, 'author': recipe.author,
            'following_recipe': following_recipe, "t":t, 'range': range(3) }) # noqa


def author_recipe(request, username):
    recepe_author = get_object_or_404(User, username=username)
    recipe_list = recepe_author.recipes.all()
    paginator = Paginator(recipe_list, 5)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    user = request.user
    if user.is_authenticated:
        following = FollowUser.objects.filter(
            user=user, following=recepe_author).exists()
    else:
        following = False
    return render(
            request,
            'authorRecipe.html', {
                'page': page, 'paginator': paginator, 'author': recepe_author,
                'following': following, 'count_post': paginator.count})


@login_required
def myfollow(request):
    author_list = FollowUser.objects.select_related(
        'author').filter(author__following__user=request.user)
    recipe_list = Recipe.objects.select_related('author').filter(
        author__following__user=request.user)
    paginator = Paginator(author_list, 3)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request,
                  "myFollow.html",
                  {"page": page,
                   "paginator": paginator,
                   'author_list': author_list,
                   'recipe_list': recipe_list})


class RecipeCreate(View):
    def get(self, request):
        form = RecipeForm()
        return render(request, 'formRecipe.html', {'form': form})


@login_required
def create_recipe(request):
    print(request.POST.dict())
    if request.method == 'POST':
        form = RecipeForm(request.POST, files=request.FILES or None)
        recipe_dict = request.POST.dict()
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            for i in recipe_dict:
                if i == "breakfast":
                    diet_breakfast = Diet.objects.get(slug=i)
                    recipe.diets.add(diet_breakfast)
                elif i == "lunch":
                    diet_lunch = Diet.objects.get(slug=i)
                    recipe.diets.add(diet_lunch)
                elif i == "dinner":
                    diet_dinner = Diet.objects.get(slug=i)
                    recipe.diets.add(diet_dinner)
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
    
    
    print(tag_breakfast, tag_lunch, tag_dinner)
    form = RecipeForm(
        request.POST or None, files=request.FILES or None, instance=recipe)
    if form.is_valid():
        form.save()
        return redirect(
            'recipe', username=request.user.username, recipe_id=recipe_id)
    
    return render(
        request, 'formChangeRecipe.html',
        {'form': form, 'recipe': recipe,
        'tag_breakfast': tag_breakfast,
        'tag_dinner': tag_dinner,
        'tag_lunch': tag_lunch})


def shop_list(request):
    count_purchase = Purchases.objects.all().count()
    purchases = Purchases.objects.all()
    return render(
        request, 'shopList.html', {
            "purchases": purchases,
            "count_purchase": count_purchase})
