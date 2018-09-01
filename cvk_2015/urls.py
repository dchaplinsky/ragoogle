from django.urls import path
from django.conf.urls import url
from .views import CVK2015DetailsView

urlpatterns = [
    path('<pk>', CVK2015DetailsView.as_view(), name="cvk_2015>details"),
]

