from django.apps import apps as django_apps

_ENABLED_ELASTIC_MODELS = None


def get_all_enabled_models():
    global _ENABLED_ELASTIC_MODELS
    if _ENABLED_ELASTIC_MODELS is not None:
        return _ENABLED_ELASTIC_MODELS

    _ENABLED_ELASTIC_MODELS = []
    for config in django_apps.app_configs.values():
        if hasattr(config, "elastic_model"):
            _ENABLED_ELASTIC_MODELS.append(config.elastic_model)

    return _ENABLED_ELASTIC_MODELS


def get_all_enabled_indices():
    return [model._doc_type.index for model in get_all_enabled_models()]
