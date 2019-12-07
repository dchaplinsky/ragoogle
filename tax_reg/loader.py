from abstract.loaders import FileLoader

from django.utils import timezone
from dateutil.parser import parse as dt_parse
from dateutil.relativedelta import relativedelta
import jmespath


class TaxRegLoader(FileLoader):
    filetype = "csv"
    last_updated_param_is_required = False
    last_updated_path = "company_reg_date"

    @property
    def model(self):
        from .models import TaxRegModel

        return TaxRegModel

    def preprocess(self, record, options):
        assert set(self.get_dedup_fields()).issubset(record.keys())

        return record

    def get_last_updated(self, obj):
        assert self.last_updated_path

        return timezone.make_aware(
            dt_parse(jmespath.search(self.last_updated_path, obj))
            + relativedelta(hours=10)
        )

    def get_dedup_fields(self):
        return ["company_edrpou"]
