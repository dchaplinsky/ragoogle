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
    help = "Calculate redflags for party finances"

    def add_arguments(self, parser):
        parser.add_argument(
            "outfile", type=argparse.FileType("wb"), help="Export rules into xlsx"
        )

    def handle(self, *args, **options):
        outfile = Workbook(options["outfile"], {"remove_timezone": True})

        qs = LetsPartyModel.objects.values_list("ultimate_recepient", "year").distinct()

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

                worksheet.write(curr_line, 0, k)
                worksheet.write(curr_line, 1, rcpt)
                worksheet.write(curr_line, 2, cnt[k])
                worksheet.write(curr_line, 3, curformat(amounts[k]))
                worksheet.write(curr_line, 4, "{:5.2f}%".format(cnt[k] / total_cnt * 100))
                if total_amount:
                    worksheet.write(curr_line, 5, "{:5.2f}%".format(amounts[k] / total_amount * 100))

        outfile.close()
