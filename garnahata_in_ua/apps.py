from django.apps import AppConfig
from .elastic_models import ElasticGarnahataModel, garnahata_idx


class GarnahataInUaConfig(AppConfig):
    name = 'garnahata_in_ua'
    verbose_name = "Реєстр власників елітної нерухомості"
    elastic_model = ElasticGarnahataModel
    elastic_index = garnahata_idx
