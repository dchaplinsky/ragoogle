import re
import logging

from django.db import models
from django.urls import reverse

from abstract.models import AbstractDataset
from abstract.tools.companies import generate_edrpou_options
from abstract.ftm_models import model as ftm_model
from names_translator.name_utils import parse_and_generate, autocomplete_suggestions
from abstract.tools.ftm import person_entity, company_entity


logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("ProcurementWinners")


class ProcurementWinnersModel(AbstractDataset):
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
        id_prefix = "procurement_winners"

        buyer = company_entity(
            name=dt["purchase"]["buyer"]["name"],
            code=dt["purchase"]["buyer"]["code"],
            address=dt["purchase"]["buyer"]["address"],
            alias=dt["purchase"]["buyer"]["name_en"],
            entity_schema="RingPublicBody",
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
            buyer.set("phone", dt["purchase"]["buyer"]["fax"])

        yield buyer

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

            cost_distpatcher_link = ftm_model.make_entity("UnknownLink")
            cost_distpatcher_link.make_id(dt["purchase"]["buyer"]["code"], dt["purchase"]["cost_dispatcher_code"])


            cost_distpatcher_link.add("subject", buyer)
            cost_distpatcher_link.add("object", cost_dispatcher)
            cost_distpatcher_link.add("role", "Розпорядник коштів")
            yield cost_distpatcher_link


        seller = company_entity(
            name=dt["seller"]["name"],
            code=dt["seller"]["code"],
            address=dt["seller"]["address"],
        )

        if dt["seller"]["phone"]:
            seller.set("phone", dt["seller"]["phone"])

        yield seller

        if dt["purchase"]["buyer"]["person"]:
            representative = person_entity(
                dt["purchase"]["buyer"]["person"],
                "Представник замовника",
                id_prefix=id_prefix + dt["purchase"]["buyer"]["code"]
            )
            yield representative

            
            representation_link = ftm_model.make_entity("Representation")
            representation_link.make_id(dt["purchase"]["buyer"]["code"], dt["purchase"]["buyer"]["person"])
            representation_link.add("agent", representative)
            representation_link.add("client", buyer)
            representation_link.add("role", "Представник замовника")
            yield representation_link


        contract = ftm_model.make_entity("Contract")
        contract.make_id(dt["purchase"]["id"])
        contract.add("authority", buyer)
        yield contract

        contract_award = ftm_model.make_entity("ContractAward")
        contract_award.make_id(dt["id"])
        contract_award.add("amount", dt["volume_uah"])
        contract_award.add("currency", "UAH")
        contract_award.add("supplier", seller)
        contract_award.add("contract", contract)

        if dt["prozorro_number"]:
            contract_award.add("lotNumber", dt["prozorro_number"][:-3])

        yield contract_award
