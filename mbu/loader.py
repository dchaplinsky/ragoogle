from abstract.loaders import FileLoader

class MbuLoader(FileLoader):
    filetype = "csv"
    last_updated_param_is_required = False
    last_updated_path = "order_date"

    @property
    def model(self):
        from .models import MbuModel
        return MbuModel

    def preprocess(self, record, options):
        assert set(self.get_dedup_fields()).issubset(
            record.keys()
        )

        return record

    def get_dedup_fields(self):
        return ["order_date", "order_no"]

