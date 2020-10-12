import re
import logging

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _

from abstract.models import AbstractDataset
from abstract.tools.companies import generate_edrpou_options
from abstract.tools.ftm import person_entity, company_entity
from abstract.ftm_models import model as ftm_model



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

    def to_entities(self):
        dt = self.data

        id_prefix = "registry_andoz_tj"

        if dt.get("section") == "individual":
            entity = person_entity(
                name=dt["name"],
                taxNumber=dt["inn"],
                idNumber=dt["ein"],
                jurisdiction="Tadjikistan",
                positions=_("Індивідуальний підприємець"),
                incorporationDate=dt["date_of_reg"],
            )
        else:
            entity = company_entity(
                name=dt["name"],
                code=dt["inn"],
                idNumber=dt["ein"],
                jurisdiction="Tadjikistan",
                incorporationDate=dt["date_of_reg"],
            )

        yield entity
