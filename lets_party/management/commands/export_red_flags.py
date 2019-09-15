import argparse
from django.core.management.base import BaseCommand, CommandError

from tqdm import tqdm
from xlsxwriter import Workbook
from lets_party.models import LetsPartyRedFlag
from abstract.tools.companies import format_edrpou


class Command(BaseCommand):
    help = "Calculate redflags for party finances"

    def add_arguments(self, parser):
        parser.add_argument(
            "outfile", type=argparse.FileType("wb"), help="Export rules into xlsx"
        )

        parser.add_argument("--only_rule", choices=LetsPartyRedFlag.RULES.keys())

    def handle(self, *args, **options):
        outfile = Workbook(options["outfile"], {"remove_timezone": True})

        worksheet = outfile.add_worksheet()
        curr_line = 0
        worksheet.write(curr_line, 0, "Транзакція")
        worksheet.write(curr_line, 1, "Дата")
        worksheet.write(curr_line, 2, "Сума")
        worksheet.write(curr_line, 3, "Донор")
        worksheet.write(curr_line, 4, "Код донора")
        worksheet.write(curr_line, 5, "Отримувач")
        worksheet.write(curr_line, 6, "Тип прапорця")
        worksheet.write(curr_line, 7, "Опис")
        worksheet.write(curr_line, 8, "Приклад порушення")

        qs = LetsPartyRedFlag.objects.select_related("transaction")

        if options["only_rule"]:
            qs = qs.filter(rule=options["only_rule"])

        for flag in tqdm(qs.iterator(), total=qs.count()):
            curr_line += 1

            worksheet.write_url(
                curr_line,
                0,
                "https://ring.org.ua{}".format(flag.transaction.get_absolute_url()),
                string="Пожертва",
            )
            worksheet.write(curr_line, 1, flag.transaction.data["donation_date"])
            worksheet.write(curr_line, 2, flag.transaction.data["amount"])
            worksheet.write(curr_line, 3, flag.transaction.data["donator_name"])
            if flag.transaction.data.get("donator_code"):
                try:
                    company_edrpou = int(flag.transaction.data["donator_code"])

                    worksheet.write_url(
                        curr_line,
                        4,
                        "https://ring.org.ua/edr/uk/company/{}".format(company_edrpou),
                        string=format_edrpou(company_edrpou),
                    )
                except ValueError:
                    pass

            worksheet.write(curr_line, 5, flag.transaction.ultimate_recepient)
            worksheet.write(curr_line, 6, flag.get_rule_display())
            worksheet.write(curr_line, 7, flag.description)
            worksheet.write(
                curr_line,
                8,
                "https://ring.org.ua/{}/{}".format(
                    flag.related_entity_source, flag.related_entity
                ),
            )

        outfile.close()
