from django.shortcuts import render, redirect, get_object_or_404
from .models import Recipe, User, FollowUser, FollowRecipe, Diet
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from .forms import RecipeForm


class Diets:
    def get_diet(self):
        return Diet.objects.all()


class RecipesView(Diets, ListView):
    """Список """
    model = Recipe
    queryset = Recipe.objects.all()
    paginate_by = 5


class FilterDietView(Diets, ListView):
    """Фильтр diet"""
    def get_queryset(self):
        queryset = Recipe.objects.filter(
            diet__in=self.request.GET.getlist("diet"))
        return queryset


class Favorites_recipe(Diets, ListView):
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
    return render(
        request,
        'singlePage.html',
        {'recipe': recipe, 'author': recipe.author})


def author_recipe(request, username):
    recepe_author = get_object_or_404(User, username=username)
    recipe_list = recepe_author.recipes.all()
    paginator = Paginator(recipe_list, 10)
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
    recipe_list = Recipe.objects.select_related('author').filter(
        author__following__user=request.user)
    paginator = Paginator(recipe_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request,
                  "myFollow.html",
                  {"page": page,
                   "paginator": paginator})


@login_required
def create_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, files=request.FILES or None)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            return redirect('index')
    else:
        form = RecipeForm()
    return render(request, 'formRecipe.html', {'form': form, 'is_edit': False})


@login_required
def recipe_edit(request, username, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id, author__username=username)
    if request.user != recipe.author:
        return redirect(
            'recipe', username=request.user.username, recipe_id=recipe_id)
    form = RecipeForm(
        request.POST or None, files=request.FILES or None, instance=recipe)
    if form.is_valid():
        form.save()
        return redirect(
            'recipe', username=request.user.username, recipe_id=recipe_id)
    return render(
        request, 'formChangeRecipe.html',
        {'form': form, 'recipe': recipe, 'is_edit': True})


def shop_list(request):
    return render(request, 'shopList.html')
