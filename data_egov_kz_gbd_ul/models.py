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
logger = logging.getLogger("DataEgovKzGbdUl")


class DataEgovKzGbdUlModel(AbstractDataset):
    def get_absolute_url(self):
        return reverse('data_egov_kz_gbd_ul>details', kwargs={'pk': self.id})

    def to_dict(self):
        dt = self.data
        res = {
            "_id": self.pk,
        }

        companies = set(
            filter(None, map(
                lambda field: dt[field].strip() if dt[field] else None,
                ["id", "bin", "namekz", "nameru"],
            ))
        )

        addresses = set(
            filter(None, map(
                lambda field: dt[field].strip() if dt[field] else None,
                ["id", "bin", "addresskz", "addressru"],
            ))
        )

        persons = set([dt["director"]])

        names_autocomplete = companies | persons

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
