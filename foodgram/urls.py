from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.flatpages import views


def trigger_error(request):
    division_by_zero = 1 / 0 # noqa


urlpatterns = [
    path('sentry-debug/', trigger_error),
    path('auth/', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('about/', views.flatpage, {'url': '/about/'}, name='about'),
    path('tech/', views.flatpage, {'url': '/tech/'}, name='tech'),
    path('', include('api.urls')),
    path('', include('recipes.urls')),
]


if settings.DEBUG:

    import debug_toolbar
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT)
