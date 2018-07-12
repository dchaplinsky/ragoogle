from django.urls import path
from django.conf.urls import url
from .views import VKKSDetailsView

urlpatterns = [
    path('<pk>', VKKSDetailsView.as_view(), name="vkks>details"),
]

