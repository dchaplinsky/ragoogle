from django.urls import path
from django.conf.urls import url
from .views import LetsPartyDetailsView, LetsPartyHomeView

urlpatterns = [
    path('', LetsPartyHomeView.as_view(), name="lets_party>home"),
    path('<pk>', LetsPartyDetailsView.as_view(), name="lets_party>details"),
]

