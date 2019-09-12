import re
import logging

from django.db import models
from django.urls import reverse

from abstract.models import AbstractDataset
from abstract.tools.companies import generate_edrpou_options, deal_with_mixed_lang
from abstract.tools.ftm import person_entity, company_entity
from abstract.ftm_models import model as ftm_model
from names_translator.name_utils import parse_and_generate, autocomplete_suggestions
from jinja2_env import curformat


logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("TaxDebts")


class TaxDebtsModel(AbstractDataset):
    def get_absolute_url(self):
        return reverse("TaxDebts>details", kwargs={"pk": self.id})

    def to_dict(self):
        dt = self.data
        res = {
            "_id": self.pk,
            "last_updated_from_dataset": self.last_updated_from_dataset,
        }

        companies = set()
        addresses = set()
        persons = set()

        if dt["TIN_S"]:
            companies |= deal_with_mixed_lang(dt["NAME"])
            companies |= generate_edrpou_options(dt["TIN_S"])
            persons |= parse_and_generate(dt["PIB"], "боржник")
        else:
            persons |= parse_and_generate(dt["NAME"], "боржник")

        companies |= deal_with_mixed_lang(dt["DPI"])
        persons |= parse_and_generate(dt["DPI_BOSS"], "керівник податкової")

        names_autocomplete = (
            companies
            | autocomplete_suggestions(dt["NAME"])
            | autocomplete_suggestions(dt["PIB"])
            | autocomplete_suggestions(dt["DPI_BOSS"])
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

    def to_entities(self):
        dt = self.data

        if dt["TIN_S"]:
            debtor = company_entity(
                name=deal_with_mixed_lang(dt["NAME"]),
                code=dt["TIN_S"],
            )

            if dt["PIB"].strip():
                debtor_repr = person_entity(
                    dt["PIB"],
                    "Боржник",
                    id_prefix="tax_debts"
                )

                directorship = ftm_model.make_entity("Directorship")
                directorship.make_id(dt["TIN_S"], dt["PIB"])

                directorship.add("director", debtor_repr)
                directorship.add("organization", debtor)
                directorship.add("role", "Керівник")
                yield directorship
                yield debtor_repr
        else:
            debtor = person_entity(
                dt["NAME"],
                "Боржник",
                id_prefix="tax_debts",
            )

        debtor.set(
            "description",
            "Станом на {} ма{} податковий борг у розмірі {} тисяч грн. перед {}".format(
                self.last_updated_from_dataset.date(),
                "ло" if dt["TIN_S"] else "в/ла",
                curformat(dt["SUM_D"] + dt["SUM_M"]),
                dt["DPI"],
            ),
        )
        yield debtor

        tax_office = company_entity(
            name=deal_with_mixed_lang(dt["DPI"]),
            code=dt["DPI"],
            id_prefix="tax_debts",
            entity_type="RingPublicBody"
        )

        tax_office_head = person_entity(
            name=dt["DPI_BOSS"],
            positions="Керівник податкової інспекції",
            id_prefix="tax_debts",
            description="Станом на {} був керівником {}".format(
                self.last_updated_from_dataset.date(),
                dt["DPI"],
            )
        )

        tax_office_directorship = ftm_model.make_entity("Directorship")
        tax_office_directorship.make_id(dt["DPI"], dt["DPI_BOSS"])

        tax_office_directorship.add("director", tax_office_head)
        tax_office_directorship.add("organization", tax_office)
        tax_office_directorship.add("role", "Керівник")

        yield tax_office_directorship
        yield tax_office
        yield tax_office_head

        debt = ftm_model.make_entity("RingDebt")
        debt.make_id(self.pk, "debt")

        debt.add("debtor", debtor)
        debt.add("creditor", tax_office)
        debt.add("amount", round((dt["SUM_D"] + dt["SUM_M"]) * 1000, 2))
        debt.add("currency", "UAH")

        yield debt
