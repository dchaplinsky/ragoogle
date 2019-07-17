from django.urls import path
from django.conf.urls import url
from .views import TaxDebtsDetailsView

urlpatterns = [
    path('<pk>', TaxDebtsDetailsView.as_view(), name="tax_debts>details"),
]

