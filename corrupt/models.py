import re
import logging

from django.db import models
from django.urls import reverse

from abstract.models import AbstractDataset
from abstract.tools.companies import generate_edrpou_options
from names_translator.name_utils import generate_all_names, autocomplete_suggestions, concat_name


logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("Corrupt")


class CorruptModel(AbstractDataset):
    def get_absolute_url(self):
        return reverse("corrupt>details", kwargs={"pk": self.id})

    def to_dict(self):
        dt = self.data
        res = {"_id": self.pk}

        companies = set(dt["CORR_WORK_PLACE"])
        addresses = set()
        persons = set()

        persons |= generate_all_names(
            dt["CORRUPTIONER_LAST_NAME"], dt["CORRUPTIONER_FIRST_NAME"], dt["CORRUPTIONER_SURNAME"], "Корупціонер"
        )

        names_autocomplete = autocomplete_suggestions(
            concat_name(dt["CORRUPTIONER_LAST_NAME"], dt["CORRUPTIONER_FIRST_NAME"], dt["CORRUPTIONER_SURNAME"])
        )


        raw_records = set(
            [
                dt["CORR_WORK_POS"],
                dt["ACTIVITY_SPH_NAME"],
                dt["OFFENSE_NAME"],
                dt["PUNISHMENT"],
                dt["COURT_CASE_NUM"],
                dt["SENTENCE_NUMBER"],
                dt["CODEX_ARTICLES_LIST_CODEX_ART_NUMBER"],
                dt["CODEX_ARTICLES_LIST_CODEX_ART_NAME"],
            ]
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
