from django.urls import path
from django.conf.urls import url
from .views import DabiRegistryDetailsView

urlpatterns = [
    path('<pk>', DabiRegistryDetailsView.as_view(), name="dabi_registry>details"),
]

