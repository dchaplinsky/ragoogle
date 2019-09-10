import bz2
import os.path
import re
import sys
import argparse
import tqdm
from functools import partial
from itertools import zip_longest, chain
from multiprocessing import Pool
from elasticsearch.exceptions import SerializationError
from django.apps import apps as django_apps
from django.conf import settings
from django.core.management.base import BaseCommand
from elasticsearch.serializer import JSONSerializer
from django.utils import timezone
from abstract.ftm_models import get_degradation_mapping
from followthemoney import model as base_ftm_model

from search.search_tools import get_apps_with_data_model
from search.models import get_datasource_pages


def grouper(iterable, n, fillvalue=None):
    """Collect data into fixed-length chunks or blocks"""
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


class Command(BaseCommand):
    json = JSONSerializer()
    degradation_mapping = get_degradation_mapping()
    help = "Export indexed documents into machinereadable format"

    def add_arguments(self, parser):
        parser.add_argument("--from", default=0, type=int)
        parser.add_argument("--to", default=None, type=int)
        parser.add_argument(
            "--degrade_to_basic_ftm", default=False, action="store_true"
        )
        parser.add_argument("--outfile", type=str)
        parser.add_argument("--save_index_file", type=str)
        parser.add_argument("--threads", type=int, default=settings.NUM_THREADS)
        parser.add_argument("--batch_size", type=int, default=200)

        parser.add_argument(
            "datasource",
            choices=get_apps_with_data_model(),
            help="Which source should be exported",
        )

    @classmethod
    def to_entities(cls, rec, degrade):
        res = []
        for ftm in rec.to_entities():
            if degrade:
                ftm.schema = cls.degradation_mapping[ftm.schema.name]

            res.append(cls.json.dumps(ftm.to_dict()))

        return res

    def handle(self, *args, **options):
        if "datasource" not in options:
            self.stderr.write("You need to specify datasource to export")
            return

        config = django_apps.app_configs[options["datasource"]]
        Model = config.data_model

        qs = Model.objects.all()
        if options["from"] and options["to"] is not None:
            qs = qs[options["from"] : options["to"]]
        else:
            if options["from"]:
                qs = qs[options["from"] :]
            elif options["to"] is not None:
                qs = qs[: options["to"]]

        total = qs.count()

        out_fp = sys.stdout
        if options["outfile"]:
            if options["outfile"].endswith(".bz2"):
                out_fp = bz2.open(options["outfile"], "wt")
            else:
                out_fp = open(options["outfile"], "w")

        pool = Pool(options["threads"])

        with tqdm.tqdm(total=total) as pbar:
            for chunk in grouper(qs.iterator(), options["batch_size"]):
                for ftm in chain.from_iterable(
                    pool.imap(
                        partial(
                            Command.to_entities, degrade=options["degrade_to_basic_ftm"]
                        ),
                        filter(None, chunk),
                    )
                ):
                    out_fp.write(ftm + "\n")

                pbar.update(len(chunk))

        if options["save_index_file"]:
            index_data = {}

            if os.path.exists(options["save_index_file"]):
                with open(options["save_index_file"], "r") as fp:
                    try:
                        index_data = {
                            d["dataset_id"]: d for d in self.json.loads(fp.read())
                        }
                    except SerializationError:
                        self.stderr.write("Cannot load index file, recreating it")

            index_data[options["datasource"]] = {
                "foreign_id": "ua_{}".format(options["datasource"]),
                "country": "Ukraine",
                "dataset_id": options["datasource"],
                "records": total,
                "last_updated": timezone.now(),
                "information_url": "https://ring.org.ua",
                "publisher": "Проект ring.org.ua",
                "publisher_url": "https://ring.org.ua",
            }

            if os.path.exists(options["outfile"]):
                index_data[options["datasource"]]["dump_url"] = options["outfile"]

            pages = get_datasource_pages()
            if options["datasource"] in pages:
                page = pages[options["datasource"]]
                index_data[options["datasource"]].update(
                    {
                        "information_url": "https://ring.org.ua{}".format(
                            page.get_absolute_url()
                        ),
                        "category": page.category,
                        "source_url": page.url,
                        "description": page.description,
                        "description_en": page.description_en,
                        "credits": page.credits,
                    }
                )

            with open(options["save_index_file"], "w") as fp:
                fp.write(self.json.dumps(list(index_data.values())))
