from django.urls import path
from django.conf.urls import url
from .views import TaxRegDetailsView

urlpatterns = [
    path('<pk>', TaxRegDetailsView.as_view(), name="tax_reg>details"),
]

