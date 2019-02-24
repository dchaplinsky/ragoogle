import re
import argparse
from collections import defaultdict

from abstract.loaders import FileLoader


class CompanyHouseUaLoader(FileLoader):
    filetype = "csv"
    last_updated_param_is_required = True

    @property
    def model(self):
        from .models import CompanyHouseUaModel
        return CompanyHouseUaModel

    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)

    def preprocess(self, record, options):
        record["name_lowered"] = record["name"].lower()
        record["occupation_or_role"] = record["occupation"] or record["role"]

        assert set(self.get_dedup_fields()).issubset(
            record.keys()
        )

        return record

    def get_dedup_fields(self):
        return ["company_number", "name_lowered", "occupation_or_role"]

