from abstract.loaders import FileLoader

class CVK2015Loader(FileLoader):
    filetype = "csv"
    last_updated_param_is_required = False

    @property
    def model(self):
        from .models import CVK2015Model
        return CVK2015Model

    def preprocess(self, record, options):
        assert set(self.get_dedup_fields()).issubset(
            record.keys()
        )

        return record

    def get_dedup_fields(self):
        return [
            "name",
            "body",
            "description",
            "party"
        ]

