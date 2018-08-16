import logging

from django.db import models
from django.urls import reverse

from abstract.models import AbstractDataset
from names_translator.name_utils import (
    generate_all_names,
    autocomplete_suggestions,
    concat_name,
)

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("vkks")


class VKKSModel(AbstractDataset):
    def get_absolute_url(self):
        return reverse('vkks>details', kwargs={'pk': self.pk})

    def to_dict(self):
        dt = self.data
        dt_g = dt["general"]
        res = {
            "_id": self.pk,
            "last_updated_from_dataset": self.last_updated_from_dataset,
            "first_updated_from_dataset": self.first_updated_from_dataset,
        }

        names_autocomplete = set()
        addresses = set()
        companies = set()
        persons = set()

        persons |= generate_all_names(
            dt_g["last_name"], dt_g["name"], dt_g["patronymic"], dt_g["post"]["post"]
        )
        names_autocomplete |= autocomplete_suggestions(
            concat_name(dt_g["last_name"], dt_g["name"], dt_g["patronymic"])
        )

        companies.add(dt_g["post"]["office"])

        for fam in dt_g["family"]:
            persons |= generate_all_names(
                fam["last_name"], fam["name"], fam["patronymic"], fam["relation"]
            )
            names_autocomplete |= autocomplete_suggestions(
                concat_name(fam["last_name"], fam["name"], fam["patronymic"])
            )

            for career in fam["career"]:
                companies.add(career["workplace"])

        for fam in dt_g["family_conflicts"]:
            anything_new = autocomplete_suggestions(
                concat_name(fam["last_name"], fam["name"], fam["patronymic"])
            )
            if anything_new and not anything_new.issubset(names_autocomplete):
                persons |= generate_all_names(
                    fam["last_name"], fam["name"], fam["patronymic"], "Пов'язана особа"
                )
                logger.warning("Oh wow, second section has persons missing from first one {}".format(anything_new))
                names_autocomplete |= anything_new

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
