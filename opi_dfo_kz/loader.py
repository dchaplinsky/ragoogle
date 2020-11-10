from abstract.loaders import FileLoader

class OpiDfoKzLoader(FileLoader):
    filetype = "mongo"
    mongo_collection = "opi_dfo_kz"
    last_updated_param_is_required = False
    last_updated_path = "scraping_date"

    @property
    def model(self):
        from .models import OpiDfoKzModel
        return OpiDfoKzModel

    def preprocess(self, record, options):
        assert set(self.get_dedup_fields()).issubset(
            record.keys()
        )

        return record

    def get_dedup_fields(self):
        return ["bin", "rnn"]

