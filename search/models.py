from django.db import models
from django.contrib.postgres.fields import JSONField
from django.urls import reverse
from django.utils.translation import gettext as _

from ckeditor.fields import RichTextField

from search.search_tools import get_all_enabled_datasources

class NamesDict(models.Model):
    id = models.CharField(_("Хеш"), max_length=40, primary_key=True)
    term = models.CharField(_("Термін"), max_length=255, db_index=True)
    translation = models.CharField(_("Переклад"), max_length=255)
    rec_type = models.IntegerField(
        "Тип запису", choices=((0, _("Слово")), (1, _("Фраза"))), db_index=True
    )
    comment = models.CharField(_("Опис набору даних"), max_length=100)


class DataSource(models.Model):
    CATEGORIES = {
        "news": "News archives",
        "leak": "Leaks",
        "land": "Land registry",
        "gazette": "Gazettes",
        "court": "Court archives",
        "company": "Company registries",
        "sanctions": "Sanctions lists",
        "procurement": "Procurement",
        "finance": "Financial records",
        "grey": "Grey literature",
        "library": "Document libraries",
        "license": "Licenses and concessions",
        "regulatory": "Regulatory filings",
        "poi": "Persons of interest",
        "customs": "Customs declarations",
        "census": "Population census",
        "transport": "Air and maritime registers",
        "other": "Other material",
    }
    slug = models.CharField(
        _("Ідентифікатор датасету"),
        max_length=50,
        primary_key=True,
        choices=((k, v.verbose_name) for k, v in get_all_enabled_datasources().items()),
    )
    name = models.TextField(_("Назва датасету"))
    url = models.URLField(_("Джерело походження"), blank=True)
    description = RichTextField(_("Опис набору даних"), blank=True)
    description_en = RichTextField(_("Опис набору даних (in English)"), blank=True)
    credits = RichTextField(_("Хто надав набір даних"), blank=True)
    category = models.CharField(_("Тип датасету в класифікації OCCRP"), choices=CATEGORIES.items(), max_length=15)

    def get_absolute_url(self):
        return reverse('about_datasource', kwargs={'slug': self.slug})


_DATASOURCE_PAGES = None

def get_datasource_pages():
    global _DATASOURCE_PAGES
    if _DATASOURCE_PAGES is not None:
        return _DATASOURCE_PAGES

    _DATASOURCE_PAGES = {ds.slug: ds for ds in DataSource.objects.all()}

    return _DATASOURCE_PAGES

