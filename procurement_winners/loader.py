from abstract.loaders import FileLoader


class ProcurementWinnersLoader(FileLoader):
    filetype = "jsonlines"
    last_updated_path = "date"

    @property
    def model(self):
        from .models import ProcurementWinnersModel

        return ProcurementWinnersModel

    def preprocess(self, record, options):
        assert set(self.get_dedup_fields()).issubset(record.keys())

        return record

    def get_payload_for_create(self, item, doc_hash, **kwargs):
        params = super().get_payload_for_create(item, doc_hash, **kwargs)

        params.update({
            "winner_name": item["seller"]["name"],
            "winner_code": int(item["seller"]["code"].lstrip("0")),
        })

        return params

    def get_dedup_fields(self):
        return ["id"]
