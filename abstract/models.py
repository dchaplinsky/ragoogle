from django.db import models
from django.contrib.postgres.fields import JSONField

from ckeditor.fields import RichTextField


class DataSource(models.Model):
    slug = models.CharField("Ідентифікатор датасету", max_length=50, primary_key=True)
    name = models.TextField("Назва датасету")
    url = models.URLField("Джерело походження", blank=True)
    description = RichTextField("Опис набору даних", blank=True)


class AbstractDataset(models.Model):
    id = models.CharField("Хеш", max_length=40, primary_key=True)
    data = JSONField(verbose_name="Дані", null=True)

    last_updated_from_dataset = models.DateTimeField(
        verbose_name="Останній раз завантажено", null=True)
    first_updated_from_dataset = models.DateTimeField(
        verbose_name="Перший раз завантажено", null=True)

    def to_dict(self):
        raise NotImplementedError()

    class Meta:
        abstract = True
