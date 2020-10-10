import re
import logging

from django.db import models
from django.urls import reverse

from abstract.models import AbstractDataset
from abstract.tools.companies import generate_edrpou_options
from names_translator.name_utils import parse_and_generate, autocomplete_suggestions


logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("RegistryAndozTj")


class RegistryAndozTjModel(AbstractDataset):
    def get_absolute_url(self):
        return reverse("registry_andoz_tj>details", kwargs={"pk": self.id})

    def to_dict(self):
        dt = self.data
        res = {
            "_id": self.pk,
            "last_updated_from_dataset": self.last_updated_from_dataset,
            "first_updated_from_dataset": self.first_updated_from_dataset,
        }

        companies = set(
            [
                dt["ein"].strip("\xa0"),
                dt["inn"].strip("\xa0"),
            ]
        )

        persons = set()
        if not dt.get("date_of_reg", "").strip("\xa0"):
            del dt["date_of_reg"]


        if dt.get("section") == "individual":
            persons.add(dt["name"])
        else:
            companies.add(dt["name"])

        names_autocomplete = companies | persons

        res.update(dt)
        res.update(
            {
                "companies": list(filter(None, companies)),
                "addresses": [],
                "persons": list(filter(None, persons)),
                "names_autocomplete": list(filter(None, names_autocomplete)),
            }
        )

        return res
