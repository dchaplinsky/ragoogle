from django.urls import path
from django.conf.urls import url
from .views import LetsPartyDetailsView

urlpatterns = [
    path('<pk>', LetsPartyDetailsView.as_view(), name="lets_party>details"),
]

