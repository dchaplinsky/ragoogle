from abstract.loaders import FileLoader

class Gr5GosreestrKzLoader(FileLoader):
    filetype = "mongo"
    mongo_collection = "gr5_gosreestr_kz"
    last_updated_param_is_required = False
    last_updated_path = "scraping_date"

    @property
    def model(self):
        from .models import Gr5GosreestrKzModel
        return Gr5GosreestrKzModel

    def preprocess(self, record, options):
        assert set(self.get_dedup_fields()).issubset(
            record.keys()
        )

        return record

    def get_dedup_fields(self):
        return ["bin"]

