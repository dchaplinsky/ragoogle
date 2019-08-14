import re
import logging

from django.db import models
from django.urls import reverse

from abstract.models import AbstractDataset
from abstract.tools.companies import generate_edrpou_options
from names_translator.name_utils import (
    parse_and_generate,
    autocomplete_suggestions
)


logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("LetsParty")


class LetsPartyModel(AbstractDataset):
    TYPES = {
        "nacp": "Звіти партій (НАЗК)",
        "parliament": "Попередні звіти парламентських виборів (ЦВК)",
        "president": "Попередні звіти президентських виборів (ЦВК)",
        "parliament_final": "Звіти парламентських виборів (ЦВК)",
        "president_final": "Звіти президентських виборів (ЦВК)",
    }
    type = models.CharField("Джерело даних", max_length=20, choices=TYPES.items())
    period = models.CharField("Період звіту", max_length=30)
    ultimate_recepient = models.CharField("Кінцевий отримувач коштів", max_length=255, db_index=True)

    def get_absolute_url(self):
        return reverse('LetsParty>details', kwargs={'pk': self.id})

    def to_dict(self):
        dt = self.data
        res = {
            "_id": self.pk,
        }

        companies = set()
        addresses = set()
        persons = set()

        names_autocomplete = companies | persons

        res.update(dt)
        res.update(
            {
                "companies": list(filter(None, companies)),
                "addresses": list(filter(None, addresses)),
                "persons": list(filter(None, persons)),
                "names_autocomplete": list(filter(None, names_autocomplete)),
            }
        )

        return res
