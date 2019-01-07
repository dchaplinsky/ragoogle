from django.urls import path
from django.conf.urls import url
from .views import DabiLicenseDetailsView

urlpatterns = [
    path('<pk>', DabiLicenseDetailsView.as_view(), name="dabi_licenses>details"),
]

