from django.urls import path
from django.conf.urls import url
from .views import OpiDfoKzDetailsView

urlpatterns = [
    path('<pk>', OpiDfoKzDetailsView.as_view(), name="opi_dfo_kz>details"),
]

