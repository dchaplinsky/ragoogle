import re

from django.contrib.staticfiles.storage import staticfiles_storage
from django.utils import formats, timezone
from django.urls import reverse
from django.utils.translation import gettext, ngettext

from dateutil.parser import parse as parse_dt
from jinja2 import Environment, evalcontextfilter, Markup, escape
from names_translator.name_utils import parse_and_generate, generate_all_names
from abstract.tools.companies import format_edrpou
from search.models import get_datasource_pages

_paragraph_re = re.compile(r"(?:\r\n|\r|\n){2,}")


def updated_querystring(request, params):
    """Updates current querystring with a given dict of params, removing
    existing occurrences of such params. Returns a urlencoded querystring."""
    original_params = request.GET.copy()
    for key in params:
        if key in original_params:
            original_params.pop(key)
    original_params.update(params)
    return original_params.urlencode()


@evalcontextfilter
def nl2br(eval_ctx, value):
    result = u"\n\n".join(
        u"<p>%s</p>" % p.strip().replace("\n", Markup("<br>\n"))
        for p in _paragraph_re.split(escape(value))
    )
    if eval_ctx.autoescape:
        result = Markup(result)
    return result


def identify_relation(rel):
    rel = rel.lower().strip()
    if rel in ["дружина", "чоловік"]:
        return "spouse"

    if rel in [
        "брат",
        "сестра",
        "двоюрідний брат",
        "двоюрідна сестра",
        "рідний брат",
        "рідна сестра",
    ]:
        return "sibling"

    if rel in ["мати", "батько"]:
        return "parent"

    if rel in ["син", "дочка", "донька", "пасинок"]:
        return "children"

    return "knows"


def curformat(value):
    value = str(value)
    if value and value != "0":
        currency = ""
        if "$" in value:
            value = value.replace("$", "")
            currency = "USD "

        if "£" in value:
            value = value.replace("£", "")
            currency = "GBP "

        if "€" in value or "Є" in value:
            value = value.replace("€", "").replace("Є", "")
            currency = "EUR "

        try:
            return (
                "{}{:,.2f}".format(currency, float(value.replace(",", ".")))
                .replace(",", " ")
                .replace(".", ",")
            )
        except ValueError:
            return value
    else:
        return ""


def ensure_aware(dt):
    if timezone.is_aware(dt):
        return dt
    else:
        return timezone.make_aware(dt)


def datetime_filter(dt, dayfirst=False):
    return (
        formats.date_format(
            timezone.localtime(
                ensure_aware(
                    parse_dt(dt, dayfirst=dayfirst) if isinstance(dt, str) else dt
                )
            ),
            "SHORT_DATETIME_FORMAT",
        )
        if dt
        else ""
    )


def date_filter(dt, dayfirst=False):
    return (
        formats.date_format(
            timezone.localtime(
                ensure_aware(
                    parse_dt(dt, dayfirst=dayfirst) if isinstance(dt, str) else dt
                )
            ),
            "SHORT_DATE_FORMAT",
        )
        if dt
        else ""
    )

def ukr_plural(value, *args):
    value = int(value) % 100
    rem = value % 10
    if value > 4 and value < 20:
        return args[2]
    elif rem == 1:
        return args[0]
    elif rem > 1 and rem < 5:
        return args[1]
    else:
        return args[2]


def environment(**options):
    env = Environment(**options)
    env.globals.update({"static": staticfiles_storage.url, "url": reverse})
    env.install_gettext_callables(gettext=gettext, ngettext=ngettext, newstyle=True)

    env.filters.update(
        {
            "datetime": datetime_filter,
            "date": date_filter,
            "nl2br": nl2br,
            "identify_relation": identify_relation,
            "curformat": curformat,
            "format_number": lambda x: "{:,d}".format(x).replace(",", " "),
            "format_edrpou": format_edrpou,
            'uk_plural': ukr_plural,
        }
    )
    env.globals.update(
        {
            "updated_querystring": updated_querystring,
            "parse_and_generate": parse_and_generate,
            "generate_all_names": generate_all_names,
            "datasource_pages": get_datasource_pages(),
        }
    )

    return env
