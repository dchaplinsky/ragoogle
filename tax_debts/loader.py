from csv import Dialect, QUOTE_MINIMAL
from abstract.loaders import FileLoader


class dialect_of_idiots(Dialect):
    delimiter = ';'
    quotechar = '"'
    doublequote = True
    skipinitialspace = False
    lineterminator = '\r\n'
    quoting = QUOTE_MINIMAL


class TaxDebtsLoader(FileLoader):
    filetype = "csv"
    encoding = "utf-8"
    csv_dialect = dialect_of_idiots
    last_updated_param_is_required = True

    @property
    def model(self):
        from .models import TaxDebtsModel
        return TaxDebtsModel

    def preprocess(self, record, options):
        assert set(self.get_dedup_fields()).issubset(
            record.keys()
        )

        record["SUM_M"] = float(record["SUM_M"].replace(",", "."))
        record["SUM_D"] = float(record["SUM_D"].replace(",", "."))

        if "" in record:
            del record[""]

        return record

    def get_dedup_fields(self):
        return ["NAME", "DPI", "SUM_D", "SUM_M"]

