from django.apps import AppConfig


class AbstractConfig(AppConfig):
    name = 'abstract'

    def to_api(self):
        return {
            "source_class": self.elastic_model.__name__,
            "name": self.name,
            "verbose_name": self.verbose_name
        }

