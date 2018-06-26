import json
from csv import DictReader
import logging
import argparse
from copy import copy
from hashlib import sha1

from django.utils import timezone

import tqdm
from dateutil.parser import parse as dt_parse


logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("importer")


class FileLoader(object):
    filetype = None
    encoding = "utf-8"
    chunk_size = 1000
    last_updated_param_is_required = False

    def get_dedup_field(self):
        raise NotImplementedError

    def preprocess(self, record):
        # NOOP
        return record

    @property
    def model(self):
        raise NotImplementedError

    def inject_params(self, parser):
        parser.add_argument(
            "dataset_file",
            type=argparse.FileType("r", encoding=self.encoding),
            help="Any dataset in the following formats: json, jsonlines, csv",
        )

        parser.add_argument(
            "--filetype",
            choices=("json", "jsonlines", "csv"),
            default=self.filetype,
            help="Format of the dataset",
        )

        parser.add_argument(
            "--last_updated_from_dataset",
            help="The date of the export of the dataset",
            required=self.last_updated_param_is_required,
        )

    def iter_dataset(self, fp, filetype):
        if filetype == "json":
            for l in json.load(fp):
                yield self.preprocess(l)

        elif filetype == "jsonlines":
            for l in fp.read():
                yield self.preprocess(json.loads(l))

        elif filetype == "csv":
            r = DictReader(fp)
            for l in r:
                yield self.preprocess(l)
        else:
            raise NotImplementedError()

    def get_name(self, doc, fields):
        return " ".join(filter(None, (doc.get(x, None) for x in fields)))

    def get_default_render_fields(self, doc, name_fields):
        return sorted(k for k in doc.keys() if k not in name_fields)

    def get_doc_hash(self, doc, options):
        dedup_fields = sorted(self.get_dedup_field())

        return sha1(
            json.dumps({k: doc.get(k) for k in dedup_fields}).encode("utf-8")
        ).hexdigest()

    def handle_details(self, *args, **options):
        pass

        if options.get("last_updated_from_dataset"):
            last_updated = timezone.make_aware(
                dt_parse(options["last_updated_from_dataset"], dayfirst=True)
            )
        else:
            last_updated = timezone.now()

        model = self.model
        existing_hashes = set(model.objects.values_list("pk", flat=True))
        bulk_add = []

        with tqdm.tqdm() as pbar:
            for item in self.iter_dataset(options["dataset_file"], options["filetype"]):
                pbar.update(1)
                doc_hash = self.get_doc_hash(item, options)
                if doc_hash not in existing_hashes:
                    bulk_add.append(
                        model(
                            id=doc_hash,
                            data=item,
                            last_updated_from_dataset=last_updated,
                            first_updated_from_dataset=last_updated,
                        )
                    )
                    existing_hashes.add(doc_hash)
                else:
                    model.objects.filter(pk=doc_hash).update(
                        data=item, last_updated_from_dataset=last_updated
                    )

                if len(bulk_add) >= self.chunk_size:
                    model.objects.bulk_create(bulk_add)
                    bulk_add = []

            # So sweet leftovers
            model.objects.bulk_create(bulk_add)
