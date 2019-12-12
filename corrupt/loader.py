from abstract.loaders import FileLoader
from csv import excel

class CorruptLoader(FileLoader):
    filetype = "csv"
    csv_dialect = excel
    # last_updated_path = "SENTENCE_DATE"

    @property
    def model(self):
        from .models import CorruptModel

        return CorruptModel

    def preprocess(self, record, options):
        assert set(self.get_dedup_fields()).issubset(record.keys())

        return record

    def get_dedup_fields(self):
        return [
            "CORRUPTIONER_LAST_NAME",
            "CORRUPTIONER_FIRST_NAME",
            "CORRUPTIONER_SURNAME",
            "COURT_CASE_NUM",
            "SENTENCE_NUMBER",
            "CORR_WORK_PLACE",
            "CODEX_ARTICLES_LIST_CODEX_ART_NUMBER",
            "SENTENCE_DATE",
        ]
