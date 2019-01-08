import re
import logging

from django.db import models
from django.urls import reverse

from abstract.models import AbstractDataset
from abstract.tools.companies import generate_edrpou_options
from names_translator.name_utils import parse_and_generate, autocomplete_suggestions


logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("dabi_registry")


def parse_edrpou(s):
    m = re.search(r"(\d{4,})", s)
    if m:
        return m.group(1)
    else:
        return ""


class DabiRegistryModel(AbstractDataset):
    def get_absolute_url(self):
        return reverse("dabi_registry>details", kwargs={"pk": self.id})

    def to_dict(self):
        dt = self.data
        res = {"_id": self.pk}

        names_autocomplete = set()
        addresses = set()
        raw_records = set(
            [dt["obj"], dt["land_plot_info"], dt["number"], dt["tech_oversee"]]
        )
        persons = set([dt["authors_oversee"]])
        companies = set(
            [
                dt["customer"].strip(" 0"),
                dt["designer"].strip(" 0"),
                dt["contractor"].strip(" 0"),
            ]
        )

        for k in ["customer", "designer", "contractor"]:
            edrpou = parse_edrpou(dt[k])
            if edrpou:
                companies |= generate_edrpou_options(edrpou)

        if ";" in dt["obj"]:
            _, adr = dt["obj"].replace("\xa0", " ").split(";", 1)
            addresses = set([adr])

        names_autocomplete |= companies

        if dt["tech_oversee"]:
            m = re.search(r"\d{2,}(\s*.*)", dt["tech_oversee"])
            if m:
                parsed = m.group(1)
                parsed = parsed.replace(";", ",")
                for p in parsed.split(","):
                    if re.search(r"\d{2,}", p) is None:
                        names_autocomplete |= parse_and_generate(p, "технічний нагляд")
                    else:
                        raw_records.add(p)

        res.update(dt)
        res.update(
            {
                "persons": list(filter(None, persons)),
                "companies": list(filter(None, [c for c in companies if not c.lower() == "фізична особа"])),
                "addresses": list(filter(None, addresses)),
                "names_autocomplete": list(filter(None, names_autocomplete)),
                "raw_records": list(filter(None, raw_records)),
            }
        )

        return res
