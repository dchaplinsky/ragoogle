from abstract.loaders import FileLoader


class ProcurementWinnersLoader(FileLoader):
    filetype = "jsonlines"
    last_updated_path = "date"

    @property
    def model(self):
        from .models import ProcurementWinnersModel

        return ProcurementWinnersModel

    def preprocess(self, record, options):
        assert set(self.get_dedup_fields()).issubset(record.keys())

        return record

    def get_dedup_fields(self):
        return ["id"]
