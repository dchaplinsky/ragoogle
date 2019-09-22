from django.urls import path
from django.conf.urls import url
from .views import LetsPartyDetailsView, LetsPartyHomeView, LetsPartyRedFlagsView

urlpatterns = [
    path('', LetsPartyHomeView.as_view(), name="lets_party>home"),
    path('redflags/<ultimate_recepient>', LetsPartyRedFlagsView.as_view(), name="lets_party>redflags"),
    path('redflags/<ultimate_recepient>/<period>', LetsPartyRedFlagsView.as_view(), name="lets_party>redflags"),
    path('<pk>', LetsPartyDetailsView.as_view(), name="lets_party>details"),
]

