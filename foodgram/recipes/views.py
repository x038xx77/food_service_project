from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Recipe, User, FollowUser, FollowRecipe, Diet, Purchases, Tag
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from .forms import RecipeForm, UploadDocumentForm
from .utils import ingredient_arrey
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
    template_name = "filter.html"
    # context_object_name = 'filter_diet'
    paginate_by = 6
    """Фильтр diet"""
    def get_queryset(self):
        queryset = Recipe.objects.filter(
            diets__in=self.request.GET.getlist('diet'))
        print("get==", self.request.GET.getlist('diet'))

        display_type = self.request.GET.getlist('diet', None)
        print(display_type)
        if (
            Tag.objects.filter(demension=display_type[0]) and
            str(display_type[0]) == str('1')
            ): # noqa
            Tag.objects.filter(demension=display_type[0]).delete()
        elif display_type[0] == str("1"):
            Tag.objects.create(
                demension=display_type[0],
                is_breakfast=True, is_lunch=False, is_dinner=False)
        elif (
            Tag.objects.filter(demension=display_type[0]) and
            str(display_type[0]) == str('2')
            ): # noqa
            Tag.objects.filter(demension=display_type[0]).delete()
        elif display_type[0] == str("2"):
            Tag.objects.create(
                demension=display_type[0],
                is_breakfast=True, is_lunch=False, is_dinner=False)
        elif (
            Tag.objects.filter(demension=display_type[0]) and
            str(display_type[0]) == str('3')
            ): # noqa
            Tag.objects.filter(demension=display_type[0]).delete()
        elif display_type[0] == str("3"):
            Tag.objects.create(
                demension=display_type[0],
                is_breakfast=True, is_lunch=False, is_dinner=False)
        return queryset


class FavoritesView(Diets, ListView):
    model = FollowRecipe
    queryset = FollowRecipe.objects.all()
    paginate_by = 6


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
    model = Recipe
    queryset = Recipe.objects.all()
    template_name = "recipes/authorRecipe.html"
    paginate_by = 6

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        recepe_author = get_object_or_404(User, username=user)
        return recepe_author.recipes.all()


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
            list_diet = []
            for i in recipe_dict:
                try:
                    if i == "breakfast":
                        diet_breakfast = Diet.objects.get(slug=i)
                        recipe.diets.add(diet_breakfast)
                        list_diet.append(i)
                    elif i == "lunch":
                        diet_lunch = Diet.objects.get(slug=i)
                        recipe.diets.add(diet_lunch)
                        list_diet.append(i)
                    elif i == "dinner":
                        diet_dinner = Diet.objects.get(slug=i)
                        recipe.diets.add(diet_dinner)
                        list_diet.append(i)
                except KeyError:
                    pass
            print("list====", len(list_diet))
            if len(ingredient_arrey(
                request.POST.dict())) == 0 or len(
                    list_diet) == 0:
                recipe.delete()
                return render(
                    request, 'formRecipe.html', {
                        'form': form, "error_ingredient": "Введите ингредиенты"
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
    print(tag_breakfast, tag_lunch, tag_dinner)
    form = RecipeForm(
        request.POST or None, files=request.FILES or None, instance=recipe)
    if form.is_valid():
        form.save()
        return redirect(
            'recipe', username=request.user.username, recipe_id=recipe_id)
    return render(
        request, 'formChangeRecipe.html',
        {
            'form': form, 'recipe': recipe, 'tag_breakfast': tag_breakfast,
            'tag_dinner': tag_dinner, 'tag_lunch': tag_lunch
        })


def shop_list(request):
    count_purchase = Purchases.objects.all().count()
    purchases = Purchases.objects.all()
    print(Recipe.objects.filter(id=43))
    for i in Recipe.objects.filter(id=43):
        print(i.ingredients)

    list_id_recipes_purchases=Purchases.objects.values_list('recipe', flat=True)
    list_purchases=[]
    for i in list_id_recipes_purchases:
        print(Recipe.objects.filter(id=i))

    return render(
        request, 'shopList.html', {
            "purchases": purchases,
            "count_purchase": count_purchase})



