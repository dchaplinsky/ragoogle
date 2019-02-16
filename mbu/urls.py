from django.urls import path
from django.conf.urls import url
from .views import MbuDetailsView

urlpatterns = [
    path('<pk>', MbuDetailsView.as_view(), name="mbu>details"),
]

