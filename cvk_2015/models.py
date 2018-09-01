import re
import logging

from django.db import models
from django.urls import reverse

from abstract.models import AbstractDataset
from names_translator.name_utils import (
    parse_and_generate,
    autocomplete_suggestions
)
from abstract.tools.countries import COUNTRIES
from abstract.tools.stocks import STOCK_TYPES


logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("cvk_2015")


class CVK2015Model(AbstractDataset):
    def get_absolute_url(self):
        return reverse('cvk_2015>details', kwargs={'pk': self.id})

    def to_dict(self):
        dt = self.data
        res = {
            "_id": self.pk,
        }

        names_autocomplete = set()
        companies = set([dt["party"]])
        persons = set()

        persons |= parse_and_generate(
            dt["name"], "Кандидат в депутати"
        )

        names_autocomplete |= autocomplete_suggestions(
            dt["name"]
        )

        if "область" in dt["body"].lower() or "київ" in dt["body"].lower():
            splits = re.split(r"область", dt["body"], flags=re.I, maxsplit=1)
            if len(splits) != 2:
                splits = re.split(r"київ", dt["body"], flags=re.I, maxsplit=1)
            
            if len(splits) == 2:
                companies.add(splits[1])
            else:
                logger.warning("Cannot parse body name out of {}".format(dt["body"]))

        names_autocomplete |= companies

        res.update(dt)

        res.update(
            {
                "companies": list(filter(None, companies)),
                "persons": list(filter(None, persons)),
                "names_autocomplete": list(filter(None, names_autocomplete)),
            }
        )

        return res
