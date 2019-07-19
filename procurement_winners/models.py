import re
import logging

from django.db import models
from django.urls import reverse

from abstract.models import AbstractDataset
from abstract.tools.companies import generate_edrpou_options
from names_translator.name_utils import parse_and_generate, autocomplete_suggestions


logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("ProcurementWinners")


class ProcurementWinnersModel(AbstractDataset):
    def get_absolute_url(self):
        return reverse("ProcurementWinners>details", kwargs={"pk": self.id})

    def to_dict(self):
        dt = self.data
        res = {"_id": self.pk, "details_url": "https://z.texty.org.ua/deal/{}".format(dt["id"])}

        companies = (
            set(
                [
                    dt["purchase"]["buyer"]["name"],
                    dt["purchase"]["buyer"]["name_en"],
                    dt["seller"]["name"],
                ]
            )
            | generate_edrpou_options(dt["purchase"]["buyer"]["code"])
            | generate_edrpou_options(dt["seller"]["code"])
            | generate_edrpou_options(dt["purchase"]["cost_dispatcher_code"])
        )

        addresses = set(
            [
                dt["seller"]["address"],
                dt["seller"]["address_full"],
                dt["purchase"]["buyer"]["address"],
                dt["purchase"]["buyer"]["address_en"],
            ]
        )

        persons = set()

        if dt["purchase"]["buyer"]["person"]:
            persons |= parse_and_generate(
                dt["purchase"]["buyer"]["person"], "Представник замовника"
            )

        raw_records = set(
            [dt["purchase"]["goods_name"], dt["purchase"]["goods_name_short"]]
        )

        names_autocomplete = companies
        if dt["purchase"]["buyer"]["person"]:
            names_autocomplete |= autocomplete_suggestions(
                dt["purchase"]["buyer"]["person"]
            )

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
