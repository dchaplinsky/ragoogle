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
logger = logging.getLogger("Mbu")


class MbuModel(AbstractDataset):
    def get_absolute_url(self):
        return reverse('Mbu>details', kwargs={'pk': self.id})

    def to_dict(self):
        dt = self.data
        res = {
            "_id": self.pk,
        }

        companies = set()
        persons = set()
        addresses = set(dt["address"])

        if re.search(r"\w\.\s?\w\.", dt["customer"]):
            for c in dt["customer"].replace(";", ",").split(","):
                if "тов" in c.lower():
                    companies.add(c.strip())
                else:
                    persons.add(c.replace(".", ". ").strip())
        else:
            companies = set([dt["customer"]])

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
