import re
import sys
import argparse
import tqdm
from django.apps import apps as django_apps
from django.core.management.base import BaseCommand
from elasticsearch.serializer import JSONSerializer
from search.search_tools import get_apps_with_data_model


class Command(BaseCommand):
    help = "Export indexed documents into machinereadable format"

    service_fields = ["names_autocomplete"]

    def add_arguments(self, parser):
        parser.add_argument("--keep_service_fields", action="store_true", default=False)

        parser.add_argument("--from", default=0, type=int)
        parser.add_argument("--to", default=None, type=int)
        parser.add_argument(
            "--outfile", nargs="?", type=argparse.FileType("w"), default=sys.stdout
        )

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
        ElasticModel = config.elastic_model
        all_docs = ElasticModel.search()

        if options["to"] is not None:
            all_docs = all_docs.query("match_all")[options["from"] : options["to"]]
            total_count = all_docs.count()
            all_docs = all_docs.execute()
        elif options["from"]:
            all_docs = all_docs.query("match_all")[options["from"] :].execute()
            total_count = all_docs.count()
            all_docs = all_docs.execute()
        else:
            total_count = all_docs.count()
            all_docs = all_docs.scan()

        for doc in tqdm.tqdm(all_docs, total=total_count):
            doc_json = doc.to_dict()
            if not options["keep_service_fields"]:
                for f in self.service_fields:
                    if f in doc_json:
                        del doc_json[f]

            options["outfile"].write(json.dumps(doc_json) + "\n")
