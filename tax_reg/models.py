import re
import logging

from django.db import models
from django.urls import reverse

from abstract.models import AbstractDataset
from abstract.tools.companies import generate_edrpou_options, deal_with_mixed_lang
from names_translator.name_utils import (
    parse_and_generate,
    autocomplete_suggestions
)


logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("TaxReg")


class TaxRegModel(AbstractDataset):
    def get_absolute_url(self):
        return reverse('tax_reg>details', kwargs={'pk': self.id})

    def to_dict(self):
        dt = self.data
        res = {
            "_id": self.pk,
            "last_updated_from_dataset": self.last_updated_from_dataset,
            "first_updated_from_dataset": self.first_updated_from_dataset,
        }

        companies = set()
        persons = set()


        companies |= generate_edrpou_options(dt["company_edrpou"])
        companies |= deal_with_mixed_lang(dt["company_name"])
        companies.add(dt["company_reg_no"])
        companies |= deal_with_mixed_lang(dt["tax_office_name"])
        addresses = set([dt["company_address"]])
        raw_records = set([dt["tax_office_code"]])

        names_autocomplete = companies | persons

        res.update(dt)
        res.update(
            {
                "companies": list(filter(None, companies)),
                "raw_records": list(filter(None, raw_records)),
                "addresses": list(filter(None, addresses)),
                "persons": list(filter(None, persons)),
                "names_autocomplete": list(filter(None, names_autocomplete)),
            }
        )

        return res
