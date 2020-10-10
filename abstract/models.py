from django.db import models
from django.db.models import JSONField
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.translation import gettext as _

from ckeditor.fields import RichTextField


class AbstractDataset(models.Model):
    id = models.CharField(_("Хеш"), max_length=40, primary_key=True)
    data = JSONField(verbose_name=_("Дані"), null=True, encoder=DjangoJSONEncoder)

    last_updated_from_dataset = models.DateTimeField(
        verbose_name=_("Останній раз завантажено"), null=True
    )
    first_updated_from_dataset = models.DateTimeField(
        verbose_name=_("Перший раз завантажено"), null=True
    )

    def to_dict(self):
        raise NotImplementedError()

    def to_entities(self):
        raise NotImplementedError()

    @classmethod
    def setup_indexing(cls):
        pass

    class Meta:
        abstract = True
