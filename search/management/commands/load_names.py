import re
import argparse
import json
from hashlib import sha1
from csv import DictReader
from collections import OrderedDict

from django.core.management.base import BaseCommand
from names_translator.name_utils import is_eng, title
from tqdm import tqdm


from search.models import NamesDict


class Command(BaseCommand):
    chunk_size = 10000

    def add_arguments(self, parser):
        parser.add_argument(
            '--wipe',
            action='store_true',
            dest='wipe',
            default=False,
            help='Wipe db table with previously imported translations',
        )

        parser.add_argument(
            'in_files',
            nargs="+",
            type=argparse.FileType("r"),
            help='Input file to index',
        )

        parser.add_argument(
            '--type',
            required=True,
            choices=["full_name", "chunk"],
            help='Type of file being imported: dict of name chunks or full names',
        )


    def get_doc_hash(self, doc):
        dct = OrderedDict({"term": doc["term"], "translation": doc["translation"]})

        return sha1(json.dumps(dct).encode("utf-8")).hexdigest()

    def normalize_term(self, term):
        return term.lower().strip(" ,.").replace("`", "'").replace("&#39", "'")

    def normalize_translation(self, term):
        return title(term.strip(" ,.").replace("`", "'").replace("&#39", "'"))


    def handle(self, *args, **options):
        if options["wipe"]:
            NamesDict.objects.all().delete()

        rec_type = (0 if options["type"] == "chunk" else 1)
        existing_hashes = set(NamesDict.objects.values_list("pk", flat=True))
        existing_hashes_len = len(existing_hashes)
        bulk_add = []

        for fp in options["in_files"]:
            r = DictReader(fp)

            for l in tqdm(r):
                if is_eng(l["translation"]) or len(l["term"]) > 30 or len(l["term"]) < 3:
                    continue
                
                doc_hash = self.get_doc_hash(l)
                if doc_hash not in existing_hashes:
                    bulk_add.append(
                        NamesDict(
                            id=doc_hash,
                            term=self.normalize_term(l["term"]),
                            translation=self.normalize_translation(l["translation"]),
                            rec_type=rec_type,
                            comment=l.get("comment", "")
                        )
                    )

                existing_hashes.add(doc_hash)

                if len(bulk_add) >= self.chunk_size:
                    NamesDict.objects.bulk_create(bulk_add)
                    bulk_add = []


        NamesDict.objects.bulk_create(bulk_add)
        self.stdout.write("Unique names loaded: {}".format(len(existing_hashes) - existing_hashes_len))
