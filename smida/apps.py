from django.apps import AppConfig
from .loader import SmidaLoader


class SmidaConfig(AppConfig):
    name = "smida"
    loader_class = SmidaLoader
