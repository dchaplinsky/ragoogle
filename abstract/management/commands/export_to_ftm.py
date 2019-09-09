import bz2
import os.path
import re
import sys
import argparse
import tqdm
from elasticsearch.exceptions import SerializationError
from django.apps import apps as django_apps
from django.core.management.base import BaseCommand
from elasticsearch.serializer import JSONSerializer
from django.utils import timezone
from followthemoney import model as base_ftm_model

from search.search_tools import get_apps_with_data_model
from search.models import get_datasource_pages


class Command(BaseCommand):
    help = "Export indexed documents into machinereadable format"

    def add_arguments(self, parser):
        parser.add_argument("--from", default=0, type=int)
        parser.add_argument("--to", default=None, type=int)
        parser.add_argument(
            "--degrade_to_basic_ftm", default=False, action="store_true"
        )
        parser.add_argument("--outfile", type=str)
        parser.add_argument("--save_index_file", type=str)

        parser.add_argument(
            "datasource",
            choices=get_apps_with_data_model(),
            help="Which source should be exported",
        )

    def handle(self, *args, **options):
        json = JSONSerializer()

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

        schemata = base_ftm_model.schemata.values()
        for rec in tqdm.tqdm(qs, total=total):
            for ftm in rec.to_entities():
                schema = ftm.schema

                if options["degrade_to_basic_ftm"]:
                    while True:
                        if schema in schemata:
                            break

                        if not ftm.schema.extends:
                            raise Exception("No basic schema found")

                        # TODO: breadth first search?
                        for parent in schema.extends:
                            if parent in schemata:
                                schema = parent
                                break

                    if schema != ftm.schema:
                        ftm.schema = schema

                out_fp.write(json.dumps(ftm.to_dict()) + "\n")

        if options["save_index_file"]:
            index_data = {}

            if os.path.exists(options["save_index_file"]):
                with open(options["save_index_file"], "r") as fp:
                    try:
                        index_data = {d["dataset_id"]: d for d in json.loads(fp.read())}
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
                fp.write(json.dumps(list(index_data.values())))
