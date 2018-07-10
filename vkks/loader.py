import re
import json
import logging

from dateutil.parser import parse as dt_parse

from names_translator.name_utils import parse_fullname
from abstract.loaders import FileLoader
from abstract.exc import ParsingError

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("importer:vkks")


class VKKSLoader(FileLoader):
    filetype = "jsonlines"

    @property
    def model(self):
        from .models import VKKSModel

        return VKKSModel

    def process_e_declaration(self, record):
        # родинних зв’язків судді за 2013–2017 роки
        year_from = record["values"].get("11")
        year_to = record["values"].get("12")
        title = record.get("date_and_type") or ""

        # TODO: Sane default?
        declaration_type = ""

        parsed_title = re.match(r"(.*)\s(\d{4})[\-–](\d{4})", title)

        if parsed_title:
            declaration_type = re.sub(r"\sза$", "", parsed_title.group(1))
            year_from = year_from or parsed_title.group(2)
            year_to = year_to or parsed_title.group(3)
        else:
            declaration_type = title
            if not year_from or not year_to:
                logger.error("Cannot parse title '{}/{}'".format(year_from, year_to))

        l, f, p, _ = parse_fullname(record["fields"]["name"])

        submit_date = dt_parse(record["submitDate"])

        res = {
            "source": "electronic",
            "ID": record["ID"],
            "intro": {
                "declaration_year_from": year_from,
                "declaration_year_to": year_to,
                "declaration_type": declaration_type,
            },
            "post": {
                "office": "{}, {}".format(
                    record["values"].get("114", {}).get("label", ""),
                    record["values"]["104"],
                ).strip(" ,"),
                "office_id": record["values"].get("114", {}).get("value"),
                "post": record["values"]["105"],
            },
            "has_information": int(record["values"]["211"]),
            "general": {
                "family": [],
                "family_conflicts": [],
                "last_name": l,
                "name": f,
                "patronymic": p,
                "family_comment": record["values"]["292"],
                "family_comment": record["values"]["392"],
            },
            "declaration": {
                "date_day": submit_date.day,
                "date_month": submit_date.month,
                "date_year": submit_date.year,
                # TODO: native object with TZ?
                "date_time": str(submit_date.time()),
            },
        }

        for pos in range(0, int(record["values"]["220"]) + 1):
            if record["values"]["220_{}-221".format(pos)]:
                fam = {}
                l, f, p, _ = parse_fullname(record["values"]["220_{}-221".format(pos)])
                fam["last_name"] = l
                fam["name"] = f
                fam["patronymic"] = p
                fam["relation"] = record["values"]["220_{}-222".format(pos)]
                fam["career"] = []

                # Trying to parse weird raw texts records for the career of the family
                # member

                # The general idea of the records in the four columns is that they 
                # are visually separated into rows, tho not always the separation looks
                # ideal even for the human eye. So, we are using plenty of heuristics 
                # below to find rows in every columns and dance around some of well known
                # corner cases (for example, no end date usually means that person still holds
                # an office)
                separator = "\n"
                if "\n" not in record["values"]["220_{}-224".format(pos)]:
                    if "__" in record["values"]["220_{}-224".format(pos)]:
                        separator = "__"
                    else:
                        separator = ","

                years_from = list(
                    filter(None, record["values"]["220_{}-225".format(pos)].split("\n"))
                )
                years_to = list(
                    filter(None, record["values"]["220_{}-226".format(pos)].split("\n"))
                )

                for x in range(4):
                    offices = list(
                        map(
                            lambda x: x.strip(" \n,_"),
                            filter(
                                None,
                                record["values"]["220_{}-223".format(pos)].split(
                                    separator * (4 - x)
                                ),
                            ),
                        )
                    )

                    positions = list(
                        map(
                            lambda x: x.strip(" \n,_"),
                            filter(
                                None,
                                record["values"]["220_{}-224".format(pos)].split(
                                    separator * (4 - x)
                                ),
                            ),
                        )
                    )

                    if len(positions) == len(years_from):
                        break

                if len(positions) != len(years_from):
                    raise ParsingError(
                        "Number of positions doesn't correspond to number of 'from' dates for {}".format(
                            res["ID"]
                        )
                    )
                if (len(years_from) - len(years_to)) > 1:
                    raise ParsingError(
                        "Number of 'from' dates doesn't correspond to number of 'to' dates for {}".format(
                            res["ID"]
                        )
                    )
                if len(positions) != len(offices) and len(offices) > 1:
                    raise ParsingError(
                        "Number of 'positions' doesn't correspond to number of 'offices' for {}".format(
                            res["ID"]
                        )
                    )

                if len(years_to) - len(years_from) > 1:
                    raise ParsingError(
                        "Number of 'to' dates has much more lines than number of 'from' dates for {}".format(
                            res["ID"]
                        )
                    )

                _parsing_quality = []
                if len(years_from) == len(years_to) == len(offices):
                    _parsing_quality.append("ideal")
                else:
                    # Here we analyzing corner cases and applying some fixes to know problems
                    # while carefully recording what we are doing and why for further visual
                    # examination
                    if len(years_from) - len(years_to) == 1:
                        _parsing_quality.append("no_end_date")
                        years_to.append("По теперішній час")

                    if len(positions) != len(offices) and len(offices) == 1:
                        _parsing_quality.append("one_office")
                        offices = [offices[0]] * len(positions)

                    if len(offices) == 0:
                        _parsing_quality.append("no_public_office")
                        offices = [""] * len(positions)

                    if len(years_to) - len(years_from) == 1:
                        _parsing_quality.append("last_date_has_two_lines")
                        years_to = years_to[:-2] + [years_to[-2] + " " + years_to[-1]]

                if not (len(years_from) == len(years_to) == len(offices)):
                    raise ParsingError("Something went very wrong when normalizing record {}".format(res["ID"]))

                for position, office, year_from, year_to in zip(positions, offices, years_from, years_to):
                    fam["_parsing_quality"] = _parsing_quality
                    fam["career"].append({
                        "position": position,
                        "workplace": office,
                        "from": year_from,
                        "to": year_to
                    })

                res["general"]["family"].append(fam)

        for pos in range(0, int(record["values"]["300"]) + 1):
            if record["values"]["300_{}-311".format(pos)]:
                fam = {}
                l, f, p, _ = parse_fullname(record["values"]["300_{}-311".format(pos)])
                fam["last_name"] = l
                fam["name"] = f
                fam["patronymic"] = p

                if record["values"]["300_{}-321".format(pos)]:
                    fam["coliving"] = "Спільно не проживаємо"
                elif record["values"]["300_{}-322".format(pos)]:
                    fam["coliving"] = "Спільно проживаємо"
                elif record["values"]["300_{}-323".format(pos)]:
                    fam["coliving"] = "Тимчасово спільно не проживаємо"
                elif record["values"]["300_{}-324".format(pos)]:
                    fam["coliving"] = "Тимчасово спільно проживаємо"

                if record["values"]["300_{}-331".format(pos)]:
                    fam["cohabiting"] = "Спільним побутом не пов’язані"
                elif record["values"]["300_{}-332".format(pos)]:
                    fam["cohabiting"] = "Пов’язані спільним побутом"
                elif record["values"]["300_{}-333".format(pos)]:
                    fam["cohabiting"] = "Тимчасово не пов’язані спільним побутом"
                elif record["values"]["300_{}-334".format(pos)]:
                    fam["cohabiting"] = "Тимчасово пов’язані спільним побутом"

                if record["values"]["300_{}-341".format(pos)]:
                    fam["mutual_liabilities"] = "Існують взаємні права та/чи обов’язки"
                elif record["values"]["300_{}-342".format(pos)]:
                    fam["mutual_liabilities"] = "Відсутні взаємні права та обов’язки"

                res["general"]["family_conflicts"].append(fam)

        return res

    def process_paper_declaration(self, record):
        if record:
            rec = record[0]["answer"]
            rec["source"] = "paper"
            rec["ID"] = record[0]["task"]["id"]

        return rec

    def preprocess(self, record, options):
        if options["source"] == "electronic":
            return self.process_e_declaration(record)
        if options["source"] == "paper":
            return self.process_paper_declaration(record)
        return record

    def inject_params(self, parser):
        super().inject_params(parser)
        parser.add_argument(
            "--source",
            choices=("paper", "electronic"),
            required=True,
            help="Source of the data (affects the conversion/parsing)",
        )

    def get_dedup_fields(self):
        return ["ID"]
