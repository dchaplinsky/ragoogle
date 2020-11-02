from django.urls import path
from django.conf.urls import url
from .views import Gr5GosreestrKzDetailsView

urlpatterns = [
    path('<pk>', Gr5GosreestrKzDetailsView.as_view(), name="gr5_gosreestr_kz>details"),
]

