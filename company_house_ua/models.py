import re
import logging
from collections import defaultdict
from itertools import product

from django.db import models
from django.urls import reverse

from abstract.models import AbstractDataset
from abstract.tools.companies import generate_edrpou_options
from search.models import NamesDict
from names_translator.name_utils import parse_and_generate, autocomplete_suggestions


logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("CompanyHouseUa")


class CompanyHouseUaModel(AbstractDataset):
    chunks_dict = defaultdict(set)
    fullnames_dict = defaultdict(set)

    @classmethod
    def setup_indexing(cls):
        for name_chunk in (
            NamesDict.objects.filter(rec_type=0).only("term", "translation").iterator()
        ):
            cls.chunks_dict[name_chunk.term.lower()].add(name_chunk.translation)
        logger.info("Loaded {} name chunks from dict".format(len(cls.chunks_dict)))

        for fullname in (
            NamesDict.objects.filter(rec_type=1).only("term", "translation").iterator()
        ):
            cls.fullnames_dict[fullname.term.lower()].add(fullname.translation)

        logger.info("Loaded {} full names from dict".format(len(cls.chunks_dict)))

    def get_absolute_url(self):
        return reverse("company_house_ua>details", kwargs={"pk": self.id})

    def to_dict(self):
        dt = self.data
        res = {"_id": self.pk}

        companies = set(
            [dt["company_number"], dt["company_name"]] + dt["company_name"].split(", ")
        )
        addresses = set([dt["address"]])
        translated_names = self.fullnames_dict.get(dt["name"].lower(), set())
        persons = set([dt["name"]]) | translated_names

        names_autocomplete = companies | persons

        translations = set(
            filter(
                None,
                map(
                    lambda x: " ".join(x),
                    product(
                        *(
                            self.chunks_dict[chunk.lower()]
                            for chunk in dt["name"].replace("-", "").split(" ")
                        )
                    ),
                ),
            )
        )

        persons |= translations
        res.update(dt)
        res.update(
            {
                "companies": list(filter(None, companies)),
                "addresses": list(filter(None, addresses)),
                "persons": list(filter(None, persons)),
                "incomplete_persons": list(filter(None, persons)),
                "translated_names": list(filter(None, translated_names)),
                "names_autocomplete": list(filter(None, names_autocomplete)),
            }
        )

        return res
