import logging
from django.db import models
from django.urls import reverse

import jmespath
from dateutil.parser import parse as dt_parse
from names_translator.name_utils import (
    parse_and_generate,
    autocomplete_suggestions,
    try_to_fix_mixed_charset
)

from abstract.models import AbstractDataset
from abstract.tools.companies import generate_edrpou_options, deal_with_mixed_lang
from abstract.tools.languages import is_eng


logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("smida_reports")


class SmidaReportModel(AbstractDataset):
    title1_jmespath = jmespath.compile("report.table[?id=='DTSTITUL_O'][].row.param")
    title2_jmespath = jmespath.compile("report.table[?id=='DTSTITLIST'].row.param")
    title3_jmespath = jmespath.compile("report.table[?id=='ROOT'].row.param")
    current_persons_jmespath = jmespath.compile(
        "report.table[?id=='DTSPERSON_P'].row[].param"
    )
    fired_persons_jmespath = jmespath.compile(
        "report.table[?id=='DTSPERSON_O'].row[].param"
    )

    def get_absolute_url(self):
        return reverse("smida_report>details", kwargs={"pk": self.id})

    def to_dict(self):
        dt = self.data
        res = {
            "_id": self.pk,
            "report_id": dt["report"]["id"],
            "timestamp": dt_parse(dt["report"]["timestamp"]),
            "last_updated_from_dataset": self.last_updated_from_dataset,
            "first_updated_from_dataset": self.first_updated_from_dataset,
        }

        names_autocomplete = set()
        companies = set()
        persons = set()
        addresses = set()

        title1 = self.title1_jmespath.search(dt)
        title2 = self.title2_jmespath.search(dt)
        report_title = self.title3_jmespath.search(dt)[0]

        report_title["STD"] = dt_parse(report_title["STD"])
        report_title["FID"] = dt_parse(report_title["FID"])

        titles = title1 + title2
        if titles:
            title = titles[0]

            address = ", ".join(
                filter(
                    None,
                    [
                        title.get("E_CONT"),
                        title.get("E_ADRES"),
                        title.get("E_POST"),
                        title.get("E_RAYON"),
                        title.get("E_STREET"),
                    ],
                )
            )
            addresses.add(address)

            res["detailed_title"] = title
            companies |= deal_with_mixed_lang(title.get("E_NAME"))

            if title.get("FIO_PODP"):
                for p in deal_with_mixed_lang(title["FIO_PODP"]):
                    persons |= parse_and_generate(
                        p, title["POS_PODP"] or ""
                    )

                    names_autocomplete |= autocomplete_suggestions(p)

        res["report_title"] = report_title
        companies |= generate_edrpou_options(report_title.get("D_EDRPOU"))
        companies |= deal_with_mixed_lang(report_title.get("D_NAME"))

        associates = self.current_persons_jmespath.search(dt)
        dismissed_associates = self.fired_persons_jmespath.search(dt)

        res["associates"] = associates
        res["dismissed_associates"] = dismissed_associates

        for assoc in associates + dismissed_associates:
            assoc["DAT_PASP"] = assoc.get("DAT_PASP")
            if assoc["DAT_PASP"]:
                assoc["DAT_PASP"] = dt_parse(assoc["DAT_PASP"])

            full_name = assoc.get("P_I_B", "") or ""

            if full_name.strip():
                parsed_name = ""
                parsed_chunks = []

                # TODO: better word splitting
                for chunk in full_name.split():
                    # TODO: better detection of latin
                    chunk = try_to_fix_mixed_charset(chunk)

                    if (
                        is_eng(chunk)
                        or chunk.startswith("(")
                        or chunk.endswith(")")
                        or chunk in "-"
                        or chunk.startswith("-")
                    ):
                        break
                    elif chunk:
                        parsed_chunks.append(chunk)

                # Looks like real person
                if len(parsed_chunks) in [2, 3]:
                    persons |= parse_and_generate(
                        " ".join(parsed_chunks), assoc.get("POSADA", "") or ""
                    )

                    names_autocomplete |= autocomplete_suggestions(" ".join(parsed_chunks))

                    persons |= parse_and_generate(
                        full_name, assoc.get("POSADA", "") or ""
                    )
                    names_autocomplete |= autocomplete_suggestions(full_name)
                else:
                    companies.add(" ".join(parsed_chunks))
                    companies |= deal_with_mixed_lang(full_name)


        names_autocomplete |= companies

        res.update(
            {
                "companies": list(filter(None, companies)),
                "addresses": list(filter(None, addresses)),
                "persons": list(filter(None, persons)),
                "names_autocomplete": list(filter(None, names_autocomplete)),
            }
        )

        return res
