from django.apps import apps as django_apps

_ENABLED_DATASOURCES = None


def get_all_enabled_datasources():
    global _ENABLED_DATASOURCES
    if _ENABLED_DATASOURCES is not None:
        return _ENABLED_DATASOURCES

    _ENABLED_DATASOURCES = {}
    for app_label, config in django_apps.app_configs.items():
        if hasattr(config, "elastic_model"):
            _ENABLED_DATASOURCES[app_label] = config

    return _ENABLED_DATASOURCES


def get_all_enabled_models(filter_by=None):
    filter_by = filter_by or None

    return [
        config.elastic_model
        for config in get_all_enabled_datasources().values()
        if (filter_by is None) or (config.name in filter_by)
    ]


def get_all_enabled_indices(filter_by=None):
    return [model._doc_type.index for model in get_all_enabled_models(filter_by)]


def get_all_doctypes(filter_by=None):
    filter_by = filter_by or None

    return {
        config.elastic_model._doc_type.name: config
        for config in get_all_enabled_datasources().values()
        if (filter_by is None) or (config.name in filter_by)
    }


def get_apps_with_loader():
    ds = get_all_enabled_datasources()
    return [k for k, config in ds.items() if hasattr(config, "loader_class")]


def get_apps_with_data_model():
    ds = get_all_enabled_datasources()
    return [k for k, config in ds.items() if hasattr(config, "data_model")]

