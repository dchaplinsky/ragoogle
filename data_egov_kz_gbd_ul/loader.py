from abstract.loaders import FileLoader

class DataEgovKzGbdUlLoader(FileLoader):
    filetype = "mongo"
    mongo_collection = "data_egov_kz_gbd_ul"
    last_updated_param_is_required = False
    last_updated_path = "scraping_date"

    @property
    def model(self):
        from .models import DataEgovKzGbdUlModel
        return DataEgovKzGbdUlModel

    def preprocess(self, record, options):
        assert set(self.get_dedup_fields()).issubset(
            record.keys()
        )

        return record

    def get_dedup_fields(self):
        return ["id"]

