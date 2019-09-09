from django.db import models
from django.contrib.postgres.fields import JSONField
from ckeditor.fields import RichTextField


class AbstractDataset(models.Model):
    id = models.CharField("Хеш", max_length=40, primary_key=True)
    data = JSONField(verbose_name="Дані", null=True)

    last_updated_from_dataset = models.DateTimeField(
        verbose_name="Останній раз завантажено", null=True
    )
    first_updated_from_dataset = models.DateTimeField(
        verbose_name="Перший раз завантажено", null=True
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
