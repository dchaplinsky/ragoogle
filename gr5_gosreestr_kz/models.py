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
logger = logging.getLogger("Gr5GosreestrKz")


class Gr5GosreestrKzModel(AbstractDataset):
    def get_absolute_url(self):
        return reverse('gr5_gosreestr_kz>details', kwargs={'pk': self.id})

    def to_dict(self):
        dt = self.data
        res = {
            "_id": self.pk,
            "last_updated_from_dataset": self.last_updated_from_dataset,
            "first_updated_from_dataset": self.first_updated_from_dataset,
        }

        companies = list(set(
            filter(None, map(
                lambda field: dt[field].strip() if dt[field] else None,
                ["bin", "rnn", "name_kz", "name_ru"],
            ))
        ))

        addresses = list(set(
            filter(None, map(
                lambda field: dt[field].strip() if dt[field] else None,
                ["bin", "rnn", "address"],
            ))
        ))

        for field in ["date_of_reg", "date_of_reg_init"]:
            if dt[field] and not dt.get(field, "").strip("\xa0"):
                del dt[field]

        res.update(dt)
        res.update(
            {
                "addresses": addresses,
                "companies": companies,
                "names_autocomplete": companies,
            }
        )

        return res
