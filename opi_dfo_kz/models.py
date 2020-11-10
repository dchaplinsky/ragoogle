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
logger = logging.getLogger("OpiDfoKz")


class OpiDfoKzModel(AbstractDataset):
    def get_absolute_url(self):
        return reverse('opi_dfo_kz>details', kwargs={'pk': self._id})

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

        if dt["date_of_reg"] and not dt.get("date_of_reg", "").strip("\xa0"):
            del dt["date_of_reg"]

        res.update(dt)
        res.update(
            {
                "companies": companies,
                "addresses": addresses,
                "names_autocomplete": companies,
            }
        )

        return res
