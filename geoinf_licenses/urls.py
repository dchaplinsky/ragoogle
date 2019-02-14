from django.urls import path
from django.conf.urls import url
from .views import GeoinfLicenseDetailsView

urlpatterns = [
    path('<pk>', GeoinfLicenseDetailsView.as_view(), name="geoinf_licenses>details"),
]

