from abstract.loaders import FileLoader

class GeoinfLicensesLoader(FileLoader):
    filetype = "mongo"
    mongo_collection = "geoinf_kiev_ua__licenses"
    last_updated_param_is_required = False
    last_updated_path = "start_date"

    @property
    def model(self):
        from .models import GeoinfLicenseModel
        return GeoinfLicenseModel

    def preprocess(self, record, options):
        assert set(self.get_dedup_fields()).issubset(
            record.keys()
        )

        return record

    def get_dedup_fields(self):
        return ["details_url"]

