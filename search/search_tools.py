from django.apps import apps as django_apps

_ENABLED_DATASOURCES = None


def get_all_enabled_datasources():
    global _ENABLED_DATASOURCES
    if _ENABLED_DATASOURCES is not None:
        return _ENABLED_DATASOURCES

    _ENABLED_DATASOURCES = []
    for config in django_apps.app_configs.values():
        if hasattr(config, "elastic_model"):
            _ENABLED_DATASOURCES.append(config)

    return _ENABLED_DATASOURCES


def get_all_enabled_models(filter_by=None):
    filter_by = filter_by or None

    return [
        config.elastic_model
        for config in get_all_enabled_datasources()
        if (filter_by is None) or (config.name in filter_by)
    ]


def get_all_enabled_indices(filter_by=None):
    return [model._doc_type.index for model in get_all_enabled_models(filter_by)]


def get_all_doctypes(filter_by=None):
    filter_by = filter_by or None

    return {
        config.elastic_model._doc_type.name: config
        for config in get_all_enabled_datasources()
        if (filter_by is None) or (config.name in filter_by)
    }
