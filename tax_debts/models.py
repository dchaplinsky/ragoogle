import re
import logging

from django.db import models
from django.urls import reverse

from abstract.models import AbstractDataset
from abstract.tools.companies import generate_edrpou_options, deal_with_mixed_lang
from names_translator.name_utils import parse_and_generate, autocomplete_suggestions


logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("TaxDebts")


class TaxDebtsModel(AbstractDataset):
    def get_absolute_url(self):
        return reverse("TaxDebts>details", kwargs={"pk": self.id})

    def to_dict(self):
        dt = self.data
        res = {"_id": self.pk, "last_updated_from_dataset": self.last_updated_from_dataset}

        companies = set()
        addresses = set()
        persons = set()

        if dt["TIN_S"]:
            companies |= deal_with_mixed_lang(dt["NAME"])
            companies |= deal_with_mixed_lang(dt["DPI"])
            companies |= generate_edrpou_options(dt["TIN_S"])
            persons |= parse_and_generate(dt["PIB"], "боржник")
        else:
            persons |= parse_and_generate(dt["NAME"], "боржник")
            persons |= parse_and_generate(dt["DPI_BOSS"], "керівник податкової")

        names_autocomplete = (
            companies
            | autocomplete_suggestions(dt["NAME"])
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
