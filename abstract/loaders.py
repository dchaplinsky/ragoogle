import json
from csv import DictReader
import logging
import argparse
from copy import copy
from hashlib import sha1
from collections import OrderedDict

from django.utils import timezone
from django.conf import settings
from django.db import transaction

import tqdm
import pymongo
from dateutil.parser import parse as dt_parse
import jmespath
from urllib.parse import quote_plus

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("importer")


class FileLoader(object):
    filetype = None
    encoding = "utf-8"
    chunk_size = 1000
    last_updated_param_is_required = False
    last_updated_path = None

    def __init__(self, *args, **kwargs):
        self._pathes = {}

        for k in self.get_dedup_fields():
            self._pathes[k] = jmespath.compile(k)

        return super().__init__(*args, **kwargs)


    def get_mongo_db(self):
        if settings.MONGODB_USERNAME:
            uri = "mongodb://{}:{}@{}:{}".format(
                quote_plus(settings.MONGODB_USERNAME),
                quote_plus(settings.MONGODB_PASSWORD),
                quote_plus(settings.MONGODB_HOST),
                settings.MONGODB_PORT
            )
        else:
            uri = "mongodb://{}:{}".format(
                quote_plus(settings.MONGODB_HOST),
                settings.MONGODB_PORT
            )

        connection = pymongo.MongoClient(
            uri,
            authSource=settings.MONGODB_AUTH_DB,
            **settings.MONGODB_CONNECTION_POOL_KWARGS
        )

        return connection[settings.MONGODB_DB]


    def get_dedup_fields(self):
        raise NotImplementedError

    def preprocess(self, record, options):
        # NOOP
        return record

    @property
    def model(self):
        raise NotImplementedError

    def inject_params(self, parser):
        if self.filetype != "mongo":
            parser.add_argument(
                "dataset_file",
                type=argparse.FileType("r", encoding=self.encoding),
                help="Any dataset in the following formats: json, jsonlines, csv",
            )

        parser.add_argument(
            "--filetype",
            choices=("json", "jsonlines", "csv", "mongo"),
            default=self.filetype,
            help="Format of the dataset",
        )

        parser.add_argument(
            "--mongo_collection",
            help="Mongo collection to harvest (for --filetype=mongo only)",
            type=str,
            default=getattr(self, "mongo_collection", ""),
            required=False
        )

        parser.add_argument(
            "--last_updated_from_dataset",
            help="The date of the export of the dataset",
            required=self.last_updated_param_is_required,
        )

        parser.add_argument(
            "--store_broken_to",
            help="Store records that cannot be properly parsed into a file",
            type=argparse.FileType("w", encoding=self.encoding),
        )

    def iter_dataset(self, options):
        fp = options.get("dataset_file")
        filetype = options["filetype"]

        if filetype == "mongo":
            assert options["mongo_collection"]
            db = self.get_mongo_db()
            coll = db[options["mongo_collection"]]

            for l in coll.find():
                del l["_id"]
                yield l

        elif filetype == "json":
            for l in json.load(fp):
                yield l

        elif filetype == "jsonlines":
            for l in fp:
                if l:
                    yield json.loads(l)

        elif filetype == "csv":
            r = DictReader(fp)
            for l in r:
                yield l
        else:
            raise NotImplementedError()

    def get_doc_hash(self, doc, options):
        dedup_fields = sorted(self.get_dedup_fields())

        def get_value(pth, expression):
            if not (("." in pth) or ("[" in pth) or ("]" in pth)):
                return doc[pth]

            val = expression.search(doc)

            # Evaluate if we need code below
            if isinstance(val, list):
                if len(val) == 1:
                    return v[0]
                elif len(val) == 0:
                    return None
            return val

        dct = OrderedDict((k, get_value(k, self._pathes[k])) for k in dedup_fields)

        return sha1(json.dumps(dct).encode("utf-8")).hexdigest()

    def get_last_updated(self, obj):
        assert self.last_updated_path

        return timezone.make_aware(dt_parse(jmespath.search(self.last_updated_path, obj)))

    def handle_details(self, *args, **options):
        if options.get("last_updated_from_dataset"):
            last_updated = timezone.make_aware(
                dt_parse(options["last_updated_from_dataset"], dayfirst=True)
            )
        else:
            last_updated = timezone.now()

        model = self.model
        existing_hashes = set(model.objects.values_list("pk", flat=True))
        bulk_add = []
        successful = 0
        broken = 0
        i = 0

        with tqdm.tqdm() as pbar:
            with transaction.atomic():
                for i, item in enumerate(
                    self.iter_dataset(options)
                ):
                    try:
                        item = self.preprocess(item, options)
                        if self.last_updated_path is not None:
                            try:
                                last_updated = self.get_last_updated(item)
                            except ValueError as e:
                                logger.error(
                                    "Cannot parse last_updated date in rec {}, error message was: {}".format(i, e)
                                )

                                last_updated = timezone.now()

                        successful += 1
                    except Exception as e:
                        logger.error(
                            "Cannot parse record {}, error message was: {}".format(i, e)
                        )
                        broken += 1
                        if options["store_broken_to"]:
                            options["store_broken_to"].write(json.dumps(item) + "\n")
                        continue

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
        logger.info(
            "Import of {} records done, {} successful, {} broken".format(
                i + 1, successful, broken
            )
        )


class DummyLoader(FileLoader):
    def get_dedup_fields(self):
        return []
