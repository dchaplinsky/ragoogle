from abstract.loaders import FileLoader

class DabiLicensesLoader(FileLoader):
    filetype = "mongo"
    mongo_collection = "dabi_gov_ua__licenses"
    last_updated_param_is_required = False
    last_updated_path = "start_date"

    @property
    def model(self):
        from .models import DabiLicenseModel
        return DabiLicenseModel

    def preprocess(self, record, options):
        assert set(self.get_dedup_fields()).issubset(
            record.keys()
        )

        return record

    def get_dedup_fields(self):
        return ["number"]

