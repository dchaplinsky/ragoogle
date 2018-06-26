from abstract.loaders import FileLoader

class SmidaLoader(FileLoader):
    filetype = "csv"
    last_updated_param_is_required = True

    @property
    def model(self):
        from .models import SmidaModel
        return SmidaModel

    def preprocess(self, record):
        assert set(self.get_dedup_fields()).issubset(
            record.keys()
        )

        for f in ["number_of_shares", "nominal_price", "share"]:
            record[f] = record[f].replace(",", ".")

        return record

    def get_dedup_fields(self):
        return [
            "last_name",
            "first_name",
            "patronymic",
            "EDRPOU",
            "emitent_name",
            "ICIH",
            "owner_edrpou",
            "last_name",
            "first_name",
            "patronymic",
            "type_of_stock",
            "nominal_price",
            "share",
            "number_of_shares"
        ]

