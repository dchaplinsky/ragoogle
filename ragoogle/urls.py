from django.contrib import admin
from django.apps import apps
from django.conf.urls import url, include
from django.urls import path
from django.conf import settings
from django.views.decorators.cache import cache_page
from django.contrib.sitemaps import views as sitemaps_views


from search.views import (
    HomeView,
    SearchView,
    SuggestView,
    AboutSearchView,
    AboutAPIView,
    DataSourceView,
)


sitemaps = {
    config.name: config.sitemap
    for config in apps.get_app_configs()
    if hasattr(config, "sitemap")
}

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path('about_search', AboutSearchView.as_view(), name="about_search"),
    path('api', AboutAPIView.as_view(), name="about_api"),
    path("search", SearchView.as_view(), name="search>results"),
    path("search/suggest", SuggestView.as_view(), name="search>suggest"),
    path("registry_andoz_tj/", include("registry_andoz_tj.urls")),
    path("source/<slug:slug>", DataSourceView.as_view(), name="about_datasource"),
    path("admin/", admin.site.urls),
    path(
        "sitemap.xml",
        cache_page(86400)(sitemaps_views.index),
        {"sitemaps": sitemaps, "sitemap_url_name": "sitemaps"},
    ),
    path(
        "sitemap-<section>.xml",
        cache_page(86400)(sitemaps_views.sitemap),
        {"sitemaps": sitemaps},
        name="sitemaps",
    ),
]


if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [url(r"^__debug__/", include(debug_toolbar.urls))] + urlpatterns

if settings.PROMETHEUS_ENABLE:
    urlpatterns = [url('^prometheus/', include('django_prometheus.urls'))] + urlpatterns
