import argparse
from django.core.management.base import BaseCommand, CommandError
from collections import Counter, defaultdict
from decimal import Decimal

from tqdm import tqdm
from xlsxwriter import Workbook
from lets_party.models import LetsPartyModel
from abstract.tools.companies import format_edrpou
from jinja2_env import curformat


class Command(BaseCommand):
    help = "Analyze mass donations from cities"

    big_cities = [
        "івано-франківськ",
        "дніпро",
        "дніпропетровськ",
        "кіровоград",
        "кропивницький",
        "хмельницький",
        "краматорськ",
        "запоріжжя",
        "тернопіль",
        "луганськ",
        "миколаїв",
        "чернівці",
        "чернігів",
        "вінниця",
        "донецьк",
        "житомир",
        "полтава",
        "ужгород",
        "черкаси",
        "харків",
        "херсон",
        "луцьк",
        "львів",
        "одеса",
        "рівне",
        "київ",
        "суми",
        "винница",
        "кропивницкий",
        "кировоград",
        "харьков",
        "днепр",
        "днепропетровск",
        "луганск",
        "ровно",
        "донецк",
        "луцк",
        "симферополь",
        "севастополь",
        "сімферополь",
        "хмельницкий",
        "львов",
        "сумы",
        "черкассы",
        "запорожье",
        "николаев",
        "тернополь",
        "чернигов",
        "ивано-франковск",
        "одесса",
        "черновцы",
        "киев",
    ]

    def add_arguments(self, parser):
        parser.add_argument(
            "outfile", type=argparse.FileType("wb"), help="Export rules into xlsx"
        )

    def handle(self, *args, **options):
        outfile = Workbook(options["outfile"], {"remove_timezone": True})

        qs = LetsPartyModel.objects.values_list("ultimate_recepient", "year").distinct()

        low_risk = outfile.add_format({"color": "#0000ff"})
        medium_risk = outfile.add_format({"color": "#ff8c00"})
        high_risk = outfile.add_format({"color": "#8b0000"})


        for i, (rcpt, year) in tqdm(enumerate(qs.iterator()), total=qs.count()):
            cnt = Counter()
            amounts = defaultdict(Decimal)

            for tr in (
                LetsPartyModel.objects.filter(ultimate_recepient=rcpt, year=year)
                .exclude(
                    data__donator_type__in=[
                        "гроші партії",
                        "гроші кандидата",
                        "державний бюджет",
                    ]
                )
                .only("city", "amount")
                .iterator()
            ):
                cnt[tr.city] += 1
                amounts[tr.city] += tr.amount

            worksheet = outfile.add_worksheet(f"{year}, {rcpt}"[:27] + f"…{i}")
            curr_line = 0
            worksheet.write(curr_line, 0, "Місто")
            worksheet.write(curr_line, 1, "Отримувач")
            worksheet.write(curr_line, 2, "Кількість транзакцій")
            worksheet.write(curr_line, 3, "Загальна сума")
            worksheet.write(curr_line, 4, "% транзакцій")
            worksheet.write(curr_line, 5, "% від загальної суми")

            total_cnt = sum(cnt.values())
            total_amount = sum(amounts.values())

            for k, v in cnt.most_common():
                curr_line += 1

                percent_of_transactions = cnt[k] / total_cnt * 100
                if total_amount:
                    percent_of_amount = amounts[k] / total_amount * 100
                else:
                    percent_of_amount = 0

                fmt = None
                is_big_city = k in self.big_cities

                if k:
                    if is_big_city:
                        if percent_of_transactions >= 20 or percent_of_amount >= 20:
                            fmt = high_risk
                        elif percent_of_transactions >= 15 or percent_of_amount >= 15:
                            fmt = medium_risk
                        elif percent_of_transactions >= 5 or percent_of_amount >= 5:
                            fmt = low_risk
                    else:
                        if percent_of_transactions >= 5 or percent_of_amount >= 5:
                            fmt = high_risk
                        elif percent_of_transactions >= 3 or percent_of_amount >= 3:
                            fmt = medium_risk
                        elif percent_of_transactions >= 2 or percent_of_amount >= 2:
                            fmt = low_risk

                worksheet.write(curr_line, 0, k, fmt)
                worksheet.write(curr_line, 1, rcpt, fmt)
                worksheet.write(curr_line, 2, cnt[k], fmt)
                worksheet.write(curr_line, 3, curformat(amounts[k]), fmt)
                worksheet.write(
                    curr_line, 4, "{:5.2f}%".format(percent_of_transactions), fmt
                )

                if total_amount:
                    worksheet.write(
                        curr_line, 5, "{:5.2f}%".format(percent_of_amount), fmt
                    )

        outfile.close()
