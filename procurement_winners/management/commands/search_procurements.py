import sys
import argparse
from django.core.management.base import BaseCommand, CommandError

from collections import Counter, defaultdict
from decimal import Decimal

from tqdm import tqdm
from xlsxwriter import Workbook
from elasticsearch_dsl import Search, Q, MultiSearch


from abstract.tools.companies import format_edrpou, generate_edrpou_options
from abstract.tools.misc import grouper
from jinja2_env import curformat, date_filter

from procurement_winners.elastic_models import ElasticProcurementWinnersModel


class Command(BaseCommand):
    help = "Bulk search for procurements"

    def add_arguments(self, parser):
        parser.add_argument(
            "infile",
            type=argparse.FileType("r"),
            help="List of terms to search",
            default=sys.stdin,
            nargs="?",
        )
        parser.add_argument(
            "outfile",
            type=argparse.FileType("wb"),
            help="Export procurements into xlsx",
        )

        parser.add_argument(
            "--field",
            default="purchase.buyer.code",
            help="Field (dot separated) to search in",
        )

        parser.add_argument("--batch_size", type=int, default=200)

    def handle(self, *args, **options):
        outfile = Workbook(options["outfile"], {"remove_timezone": True})
        worksheet = outfile.add_worksheet("Закупівлі")
        curr_line = 0
        worksheet.write(curr_line, 0, "Замовник")
        worksheet.write(curr_line, 1, "Код замовника")
        worksheet.write(curr_line, 2, "Переможець")
        worksheet.write(curr_line, 3, "Код переможець")
        worksheet.write(curr_line, 4, "Предмет закупівлі")
        worksheet.write(curr_line, 5, "Дата закупівлі")
        worksheet.write(curr_line, 6, "Рік")
        worksheet.write(curr_line, 7, "Очікувана сума")
        worksheet.write(curr_line, 8, "Актуальна сума")

        with tqdm() as pbar:
            for chunk in grouper(options["infile"], options["batch_size"]):
                chunk = list(filter(None, chunk))
                requests = MultiSearch()

                for l in chunk:
                    l = l.strip().strip("\u200e")
                    search = []
                    if l.isdigit():
                        search = list(generate_edrpou_options(l))
                    else:
                        search = [l]

                    q = ElasticProcurementWinnersModel.search().filter(
                        "terms", **{options["field"]: search}
                    )

                    requests = requests.add(q)

                currency_format = outfile.add_format({'num_format': '#,##0.00 ₴'})

                if len(chunk):
                    results = requests.execute()
                    for r in results:
                        for line in r:
                            curr_line += 1
                            worksheet.write(curr_line, 0, line["purchase"]["buyer"]["name"])
                            worksheet.write_url(
                                curr_line,
                                1,
                                "https://ring.org.ua/edr/uk/company/{}".format(line["purchase"]["buyer"]["code"]),
                                string=format_edrpou(line["purchase"]["buyer"]["code"]),
                            )
                            worksheet.write(curr_line, 2, line["seller"]["name"])
                            worksheet.write_url(
                                curr_line,
                                3,
                                "https://ring.org.ua/edr/uk/company/{}".format(line["seller"]["code"]),
                                string=format_edrpou(line["seller"]["code"]),
                            )
                            worksheet.write(curr_line, 4, line["purchase"]["goods_name"])
                            worksheet.write(curr_line, 5, date_filter(line["date"]))
                            worksheet.write(curr_line, 6, line["date"].year)
                            if "expected_volume" in line:
                                worksheet.write(curr_line, 7, line["expected_volume"], currency_format)
                            worksheet.write(curr_line, 8, line["volume_uah"], currency_format)

                pbar.update(len(chunk))


        outfile.close()
