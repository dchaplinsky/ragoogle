from django.urls import path
from django.conf.urls import url
from .views import DabiLicensesDetailsView

urlpatterns = [
    path('<pk>', DabiLicensesDetailsView.as_view(), name="dabi_licenses>details"),
]

