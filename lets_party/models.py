import re
import logging

from django.db import models
from django.urls import reverse

from abstract.models import AbstractDataset
from abstract.tools.companies import generate_edrpou_options
from names_translator.name_utils import parse_and_generate, autocomplete_suggestions


logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("LetsParty")


class LetsPartyModel(AbstractDataset):
    TYPES = {
        "nacp": "Звіти партій до НАЗК",
        "parliament": "Звіти парламентських виборів до ЦВК",
        "president": "Звіти президентських виборів до ЦВК",
    }
    type = models.CharField("Джерело даних", max_length=20, choices=TYPES.items())
    period = models.CharField("Період звіту", max_length=30)
    ultimate_recepient = models.CharField(
        "Кінцевий отримувач коштів", max_length=255, db_index=True
    )

    def get_absolute_url(self):
        return reverse("LetsParty>details", kwargs={"pk": self.id})

    def to_dict(self):
        dt = self.data
        res = {"_id": self.pk}

        names_autocomplete = set()
        companies = (
            set([dt["party"]])
            | generate_edrpou_options(dt["donator_code"])
            | generate_edrpou_options(dt["party"])
        )

        if dt.get("branch_code"):
            companies |= generate_edrpou_options(dt["branch_code"])

        if dt.get("branch_name"):
            companies |= generate_edrpou_options(dt["branch_name"])


        addresses = set([dt["donator_location"]])
        persons = set([dt.get("candidate_name")])

        if dt["donator_code"]:
            companies |= set([dt["donator_name"]])
        else:
            persons |= parse_and_generate(dt["donator_name"], "Донор")
            names_autocomplete |= autocomplete_suggestions(dt["donator_name"])

        names_autocomplete |= companies
        raw_records = set(
            [dt.get("account_number"), dt.get("payment_subject"), dt["transaction_doc_number"]]
        )

        res.update(dt)
        res.update(
            {
                "companies": list(filter(None, companies)),
                "addresses": list(filter(None, addresses)),
                "persons": list(filter(None, persons)),
                "names_autocomplete": list(filter(None, names_autocomplete)),
                "raw_records": list(filter(None, raw_records)),
                "type": self.get_type_display(),
                "period": self.period,
                "ultimate_recepient": self.ultimate_recepient,
            }
        )

        return res
