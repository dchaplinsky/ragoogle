import argparse
from csv import DictReader, Sniffer

from glob2 import iglob
from abstract.loaders import FileLoader


class LetsPartyLoader(FileLoader):
    filetype = "csv"
    # last_updated_param_is_required = False
    # last_updated_path = "REDEFINE ME"

    @property
    def model(self):
        from .models import LetsPartyModel
        return LetsPartyModel

    def inject_params(self, parser):
        parser.add_argument(
            "type",
            choices=self.model.TYPES.keys(),
            help="Type of dataset being imported",
        )

        parser.add_argument(
            "filemask",
            help="Glob2 filemask to find files",
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

    def preprocess(self, record, options):
        mapping = {
            "Номер розрахункового документу": "transaction_doc_number"
        }

        record["type"] = options["type"]

        record = {mapping.get(k, k): v for k, v in record.items()}

        return record

    def get_payload_for_create(self, item, doc_hash, **kwargs):
        params = super().get_payload_for_create(item, doc_hash, **kwargs)

        params.update({
            "type": item["type"],
            "ultimate_recepient": "dummy",
        })

        return params

    def get_payload_for_update(self, item, doc_hash, **kwargs):
        params = super().get_payload_for_update(item, doc_hash, **kwargs)

        params.update({
            "type": item["type"],
            "ultimate_recepient": "dummy",
        })

        return params


    def iter_dataset(self, options):
        for fname in iglob(options["filemask"]):
            with open(fname, "r", encoding=self.encoding) as fp:
                if self.csv_dialect is None:
                    dialect = Sniffer().sniff(fp.read(1024 * 16))
                    fp.seek(0)
                else:
                    dialect = self.csv_dialect

                r = DictReader(fp, dialect=dialect)
                for l in r:
                    l["type"] = options["type"]
                    yield l


    def get_dedup_fields(self):
        return ["transaction_doc_number"]
