from django.db import models
from django.contrib.postgres.fields import JSONField
from django.urls import reverse

from ckeditor.fields import RichTextField

from search.search_tools import get_all_enabled_datasources

class NamesDict(models.Model):
    id = models.CharField("Хеш", max_length=40, primary_key=True)
    term = models.CharField("Термін", max_length=255, db_index=True)
    translation = models.CharField("Переклад", max_length=255)
    rec_type = models.IntegerField(
        "Тип запису", choices=((0, "Слово"), (1, "Фраза")), db_index=True
    )
    comment = models.CharField("Опис набору даних", max_length=100)


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
        "Ідентифікатор датасету",
        max_length=50,
        primary_key=True,
        choices=((k, v.verbose_name) for k, v in get_all_enabled_datasources().items()),
    )
    name = models.TextField("Назва датасету")
    url = models.URLField("Джерело походження", blank=True)
    description = RichTextField("Опис набору даних", blank=True)
    description_en = RichTextField("Опис набору даних (in English)", blank=True)
    credits = RichTextField("Хто надав набір даних", blank=True)
    category = models.CharField("Тип датасету в класифікації OCCRP", choices=CATEGORIES.items(), max_length=15)

    def get_absolute_url(self):
        return reverse('about_datasource', kwargs={'slug': self.slug})


_DATASOURCE_PAGES = None

def get_datasource_pages():
    global _DATASOURCE_PAGES
    if _DATASOURCE_PAGES is not None:
        return _DATASOURCE_PAGES

    _DATASOURCE_PAGES = {ds.slug: ds for ds in DataSource.objects.all()}

    return _DATASOURCE_PAGES

