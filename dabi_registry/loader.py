from datetime import datetime
from django.utils import timezone
from abstract.loaders import FileLoader


class DabiRegistryLoader(FileLoader):
    filetype = "csv"
    last_updated_param_is_required = False
    last_updated_path = "not_used"

    @property
    def model(self):
        from .models import DabiRegistryModel

        return DabiRegistryModel

    def get_last_updated(self, obj):
        return timezone.make_aware(
            datetime(int(obj["year"]), int(obj["month"]), 1, 0, 0, 0)
        )

    def preprocess(self, record, options):
        assert set(self.get_dedup_fields()).issubset(record.keys())

        return record

    def get_dedup_fields(self):
        return ["number"]
