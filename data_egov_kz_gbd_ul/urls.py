from django.urls import path
from django.conf.urls import url
from .views import DataEgovKzGbdUlDetailsView

urlpatterns = [
    path('<pk>', DataEgovKzGbdUlDetailsView.as_view(), name="data_egov_kz_gbd_ul>details"),
]

