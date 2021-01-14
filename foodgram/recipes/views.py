from django.shortcuts import render, redirect, get_object_or_404
from .models import Recipe, User, FollowUser
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .forms import RecipeForm


def page_not_found(request, exception):
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )


def server_error(request):
    return render(request, "misc/500.html", status=500)


def index(request):
    recipe_list = Recipe.objects.order_by('-pub_date').all()
    paginator = Paginator(recipe_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'index.html',
        {'page': page, 'paginator': paginator}
    )


@login_required
def new_recipe(request):
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
