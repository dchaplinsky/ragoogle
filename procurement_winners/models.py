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
    winner_code = models.IntegerField("Procurement winner code", db_index=True)
    winner_name = models.CharField(blank=True, max_length=512, db_index=True)

    def get_absolute_url(self):
        return reverse("procurement_winners>details", kwargs={"pk": self.id})

    def to_dict(self):
        dt = self.data
        res = {
            "_id": self.pk,
            "details_url": "https://z.texty.org.ua/deal/{}".format(dt["id"]),
            "last_updated_from_dataset": self.last_updated_from_dataset,
            "first_updated_from_dataset": self.first_updated_from_dataset,
        }

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
                "raw_records": list(filter(None, raw_records)),
            }
        )

        return res

    def to_entities(self):
        dt = self.data

        buyer = company_entity(
            name=dt["purchase"]["buyer"]["name"],
            code=dt["purchase"]["buyer"]["code"],
            address=dt["purchase"]["buyer"]["address"],
            alias=dt["purchase"]["buyer"]["name_en"],
            entity_type="RingPublicBody",
        )

        if dt["purchase"]["buyer"]["address_en"]:
            buyer.set("address", dt["purchase"]["buyer"]["address_en"])

        if dt["purchase"]["buyer"]["name_en"]:
            buyer.set("name", dt["purchase"]["buyer"]["name_en"])

        if dt["purchase"]["buyer"]["email"]:
            buyer.set("email", dt["purchase"]["buyer"]["email"])

        if dt["purchase"]["buyer"]["phone"]:
            buyer.set("phone", dt["purchase"]["buyer"]["phone"])

        if dt["purchase"]["buyer"]["fax"]:
            buyer.set("fax", dt["purchase"]["buyer"]["fax"])

        if (
            dt["purchase"]["cost_dispatcher_code"]
            and dt["purchase"]["cost_dispatcher_name"]
            and dt["purchase"]["cost_dispatcher_code"]
            != dt["purchase"]["buyer"]["code"]
        ):
            cost_dispatcher = company_entity(
                name=dt["purchase"]["cost_dispatcher_name"],
                code=dt["purchase"]["cost_dispatcher_code"],
            )

            tax_office_directorship = ftm_model.make_entity("Directorship")
            tax_office_directorship.make_id(dt["purchase"]["buyer"]["code"], dt["purchase"]["cost_dispatcher_code"])

            tax_office_directorship.add("director", buyer)
            tax_office_directorship.add("organization", cost_dispatcher)
            yield tax_office_directorship


