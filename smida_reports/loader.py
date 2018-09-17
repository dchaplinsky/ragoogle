from abstract.loaders import FileLoader

class SmidaReportLoader(FileLoader):
    filetype = "jsonlines"
    last_updated_param_is_required = False
    last_updated_path = "report.timestamp"

    @property
    def model(self):
        from .models import SmidaReportModel
        return SmidaReportModel


    def get_dedup_fields(self):
        return [
            "report.id"
        ]

