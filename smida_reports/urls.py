from django.urls import path
from django.conf.urls import url
from .views import SmidaReportDetailsView

urlpatterns = [
    path('<pk>', SmidaReportDetailsView.as_view(), name="smida_report>details"),
]

