from django.urls import path
from django.conf.urls import url
from .views import ProcurementWinnersDetailsView

urlpatterns = [
    path('<pk>', ProcurementWinnersDetailsView.as_view(), name="procurement_winners>details"),
]

