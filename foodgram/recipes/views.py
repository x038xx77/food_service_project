from django.shortcuts import render, get_object_or_404, redirect
from .models import Recipe, Diet
from .forms import RecipeForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.urls import reverse


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
    title_href = {"title_url": "Рецепты", "href_url": "index.css"}
    return render(
        request,
        'index.html',
        title_href
    )
