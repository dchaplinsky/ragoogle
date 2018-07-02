from django.urls import path
from django.conf.urls import url
from .views import SmidaDetailsView

urlpatterns = [
    path('<pk>', SmidaDetailsView.as_view(), name="smida>details"),
]

