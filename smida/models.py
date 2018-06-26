import logging

from django.db import models

from abstract.models import AbstractDataset
from abstract.tools.names import (
    generate_all_names,
    autocomplete_suggestions,
    concat_name,
)
from abstract.tools.countries import COUNTRIES
from abstract.tools.companies import unify_cyprus_codes, generate_edrpou_options


logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("smida")


class SmidaModel(AbstractDataset):
    def to_dict(self):
        dt = self.data
        res = {
            "rec_id": self.pk,
            "last_updated_from_dataset": self.last_updated_from_dataset,
            "first_updated_from_dataset": self.first_updated_from_dataset,
        }

        names_autocomplete = set()
        countries = set()
        companies = generate_edrpou_options(dt["EDRPOU"]) | {dt["emitent_name"]}
        persons = set()

        if dt.get("country_code") in COUNTRIES:
            country = COUNTRIES[dt.get("country_code")]
            countries = {
                country["iso2"],
                country["iso3"],
                country["country_short_name"],
                country["country_name"],
                country["country_name_en"],
            }

        if dt.get("owner_edrpou") or dt.get("foreign_code"):
            # Stock owner is a company

            if dt.get("patronymic"):
                logger.warning(
                    "Record has both, code {} and patronymic {} set".format(
                        dt.get("owner_edrpou") or dt.get("foreign_code"),
                        dt.get("patronymic"),
                    )
                )

            # companies.add(dt["owner_edrpou"])
            # companies.add(dt["owner_edrpou"].lstrip("0"))
            companies |= generate_edrpou_options(dt["owner_edrpou"])
            companies |= unify_cyprus_codes(dt["foreign_code"])
            companies.add(dt["first_name"])
            companies.add(dt["last_name"])
        else:
            persons |= generate_all_names(
                dt["last_name"], dt["first_name"], dt["patronymic"], "Акціонер"
            )
            names_autocomplete |= autocomplete_suggestions(
                concat_name(dt["last_name"], dt["first_name"], dt["patronymic"])
            )

        names_autocomplete |= companies

        res.update(dt)
        res.update(
            {
                "companies": list(filter(None, companies)),
                "countries": list(filter(None, countries)),
                "persons": list(filter(None, persons)),
                "names_autocomplete": list(filter(None, names_autocomplete)),
            }
        )

        return res
