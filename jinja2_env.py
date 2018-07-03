from django.contrib.staticfiles.storage import staticfiles_storage
from django.utils import formats
from django.urls import reverse
from django.utils.translation import gettext, ngettext
from dateutil.parser import parse as parse_dt

from jinja2 import Environment


def updated_querystring(request, params):
    """Updates current querystring with a given dict of params, removing
    existing occurrences of such params. Returns a urlencoded querystring."""
    original_params = request.GET.copy()
    for key in params:
        if key in original_params:
            original_params.pop(key)
    original_params.update(params)
    return original_params.urlencode()


def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
    })
    env.install_gettext_callables(
        gettext=gettext, ngettext=ngettext, newstyle=True
    )

    env.filters.update({
        'datetime': lambda dt: formats.date_format(parse_dt(dt) if isinstance(dt, str) else dt, "SHORT_DATETIME_FORMAT"),
        'date': lambda dt: formats.date_format(parse_dt(dt) if isinstance(dt, str) else dt, "SHORT_DATE_FORMAT"),
    })
    env.globals.update({
        'updated_querystring': updated_querystring
    })

    return env
