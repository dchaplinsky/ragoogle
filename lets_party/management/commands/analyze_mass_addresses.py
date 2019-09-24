import argparse
from django.core.management.base import BaseCommand, CommandError
from collections import Counter, defaultdict
from decimal import Decimal

from tqdm import tqdm
from xlsxwriter import Workbook
from lets_party.models import LetsPartyModel
from abstract.tools.companies import format_edrpou


class Command(BaseCommand):
    help = "Calculate redflags for party finances"

    def add_arguments(self, parser):
        parser.add_argument(
            "outfile", type=argparse.FileType("wb"), help="Export rules into xlsx"
        )


    def handle(self, *args, **options):
        outfile = Workbook(options["outfile"], {"remove_timezone": True})


        qs = LetsPartyModel.objects.values_list("ultimate_recepient", "year")

        for rcpt, year in tqdm(qs.iterator(), total=qs.count()):
            cnt = Counter()
            amounts = defaultdict(Decimal)

            for tr in LetsPartyModel.objects.filter(ultimate_recepient=rcpt, year=year).iterator():
                cnt[tr.data["donator_location"]] += 1
                amounts[tr.data["donator_location"]] += tr.amount

            print(rcpt, year)
            print(cnt.most_common())
            break


        outfile.close()
