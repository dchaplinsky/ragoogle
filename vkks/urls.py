from django.urls import path
from django.conf.urls import url
from .views import VKKSDetailsView, VKKSHomeView

urlpatterns = [
    path('', VKKSHomeView.as_view(), name="vkks>home"),
    path('<pk>', VKKSDetailsView.as_view(), name="vkks>details"),
]