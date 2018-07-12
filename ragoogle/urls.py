from django.contrib import admin
from django.conf.urls import url, include
from django.urls import path
from django.conf import settings
from search.views import HomeView, SearchView, SuggestView

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('search', SearchView.as_view(), name="search>results"),
    path('search/suggest', SuggestView.as_view(), name="search>suggest"),

    path('smida/', include("smida.urls")),
    path('vkks/', include("vkks.urls")),
    path('admin/', admin.site.urls),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
