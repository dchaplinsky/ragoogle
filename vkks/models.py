import logging

from django.db import models

from abstract.models import AbstractDataset
from names_translator.name_utils import (
    generate_all_names,
    autocomplete_suggestions,
    concat_name,
)

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("vkks")


class VKKSModel(AbstractDataset):
    _DATA_SOURCES = {
        "paper": "Паперова декларація",
        "electronic": "Е-декларація",
    }

    source = models.CharField("Джерело", choices=_DATA_SOURCES.items(), max_length=10)

    def to_dict(self):
        dt = self.data
        res = {
            "_id": self.pk,
            "last_updated_from_dataset": self.last_updated_from_dataset,
            "first_updated_from_dataset": self.first_updated_from_dataset,
        }

        names_autocomplete = set()
        countries = set()
        companies = set()
        persons = set()

        res.update(dt)
        del res["date_of_report"]
        res.update(
            {
                "companies": list(filter(None, companies)),
                "countries": list(filter(None, countries)),
                "persons": list(filter(None, persons)),
                "names_autocomplete": list(filter(None, names_autocomplete)),
            }
        )

        return res
