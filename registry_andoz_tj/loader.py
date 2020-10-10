from abstract.loaders import FileLoader

class RegistryAndozTjLoader(FileLoader):
    filetype = "mongo"
    mongo_collection = "registry_andoz_tj"
    last_updated_param_is_required = False
    last_updated_path = "scraping_date"

    @property
    def model(self):
        from .models import RegistryAndozTjModel
        return RegistryAndozTjModel

    def preprocess(self, record, options):
        assert set(self.get_dedup_fields()).issubset(
            record.keys()
        )

        return record

    def get_dedup_fields(self):
        return ["ein", "inn"]

