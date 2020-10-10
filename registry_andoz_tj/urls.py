from django.urls import path
from django.conf.urls import url
from .views import RegistryAndozTjDetailsView

urlpatterns = [
    path('<pk>', RegistryAndozTjDetailsView.as_view(), name="registry_andoz_tj>details"),
]

