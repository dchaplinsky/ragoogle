from django.urls import path
from django.conf.urls import url
from .views import CompanyHouseUaDetailsView

urlpatterns = [
    path('<pk>', CompanyHouseUaDetailsView.as_view(), name="company_house_ua>details"),
]

