from django.urls import path
from django.conf.urls import url
from .views import CorruptDetailsView

urlpatterns = [
    path('<pk>', CorruptDetailsView.as_view(), name="corrupt>details"),
]

