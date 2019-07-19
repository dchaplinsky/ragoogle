from django.core.management.base import BaseCommand, CommandError
from django.apps import apps as django_apps

from elasticsearch.helpers import parallel_bulk
from elasticsearch_dsl.connections import connections
from tqdm import tqdm


class Command(BaseCommand):
    help = "Universal indexer for the datasets, stored in database"

    def add_arguments(self, parser):
        parser.add_argument(
            "--drop_indices",
            action="store_true",
            dest="drop_indices",
            default=False,
            help="Delete indices before reindex",
        )

        parser.add_argument(
            "--batch_size",
            dest="batch_size",
            type=int,
            default=400,
            help="Size of batch to send to elasticsearch",
        )

        sources = []
        for app_label, config in django_apps.app_configs.items():
            if hasattr(config, "data_model") and hasattr(config, "elastic_model"):
                sources.append(app_label)

        parser.add_argument(
            "datasource", choices=sources, help="Which source should be reindexed"
        )

    def bulk_write(self, conn, docs_to_index):
        for response in parallel_bulk(conn, (d.to_dict(True) for d in docs_to_index)):
            pass

    def handle(self, *args, **options):
        if "datasource" not in options:
            self.stderr.write("You need to specify datasource to reindex")
            return

        config = django_apps.app_configs[options["datasource"]]

        ElasticModel = config.elastic_model
        Model = config.data_model
        idx = config.elastic_index
        conn = connections.get_connection("default")

        if options["drop_indices"]:
            idx.delete(ignore=404)
            idx.create()
            ElasticModel.init()

            conn.indices.put_settings(
                index=ElasticModel._doc_type.index,
                body={"index.max_result_window": int(Model.objects.count() * 1.1 + 1)},
            )

        Model.setup_indexing()
        qs = Model.objects.all()

        docs_to_index = []
        with tqdm(total=qs.count()) as pbar:
            for p in qs.iterator():
                pbar.update(1)
                doc = p.to_dict()
                if doc is None:
                    self.stderr.write("Cannot parse {} document".format(p))
                    continue

                docs_to_index.append(ElasticModel(**doc))
                if len(docs_to_index) > options["batch_size"]:
                    self.bulk_write(conn, docs_to_index)
                    docs_to_index = []

        self.bulk_write(conn, docs_to_index)
        self.stdout.write(
            "{} of {} records indexed into ES".format(qs.count(), config.name)
        )
