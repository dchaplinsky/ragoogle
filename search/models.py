from django.db import models
from django.contrib.postgres.fields import JSONField

from ckeditor.fields import RichTextField


class NamesDict(models.Model):
    id = models.CharField("Хеш", max_length=40, primary_key=True)
    term = models.CharField("Термін", max_length=255, db_index=True)
    translation = models.CharField("Переклад", max_length=255)
    rec_type = models.IntegerField(
        "Тип запису", choices=((0, "Слово"), (1, "Фраза")), db_index=True
    )
    comment = models.CharField("Опис набору даних", max_length=100)
