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
logger = logging.getLogger("dabi_licenses")


class DabiLicenseModel(AbstractDataset):
    def get_absolute_url(self):
        return reverse('dabi_licenses>details', kwargs={'pk': self.id})

    def to_dict(self):
        dt = self.data
        res = {
            "_id": self.pk,
        }

        companies = set([dt["obj"]])
        companies |= generate_edrpou_options(dt["edrpou"])
        addresses = set([dt["address"]])

        names_autocomplete = companies

        res.update(dt)
        res.update(
            {
                "companies": list(filter(None, companies)),
                "addresses": list(filter(None, addresses)),
                "names_autocomplete": list(filter(None, names_autocomplete)),
            }
        )

        return res
