import re
import argparse
from csv import DictReader

from django.core.management.base import BaseCommand

from elasticsearch.helpers import streaming_bulk
from elasticsearch_dsl.connections import connections
from names_translator.name_utils import is_eng
from tqdm import tqdm


from search.elastic_models import Names, names_idx


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--drop_indices',
            action='store_true',
            dest='drop_indices',
            default=False,
            help='Delete indices before reindex',
        )

        parser.add_argument(
            'in_files',
            nargs="+",
            type=argparse.FileType("r"),
            help='Input file to index',
        )

    def bulk_write(self, conn, docs_to_index):
        for response in streaming_bulk(
                conn, (d.to_dict(True) for d in docs_to_index)):
            pass

    def handle(self, *args, **options):
        conn = connections.get_connection('default')

        if options["drop_indices"]:
            names_idx.delete(ignore=404)
            names_idx.create()

        docs_to_index = []
        seen = set()

        for fp in options["in_files"]:
            r = DictReader(fp)

            for l in tqdm(r):
                if is_eng(l["name"]) or len(l["name"]) > 30 or len(l["name"]) < 3:
                    continue

                if re.search(r"\d", l["name"]):
                    continue

                if l["name"].lower() in seen:
                    continue
                else:
                    seen.add(l["name"].lower())

                docs_to_index.append(Names(**l))
                if len(docs_to_index) > 10000:
                    self.bulk_write(conn, docs_to_index)
                    docs_to_index = []

        self.bulk_write(conn, docs_to_index)
        self.stdout.write("Unique names loaded: {}".format(len(seen)))
