from django.template.loader import render_to_string
from django.urls import reverse
from dateutil.parser import parse as dt_parse
from dateutil.relativedelta import relativedelta

from abstract.elastic_models import (
    BASIC_INDEX_SETTINGS,
    AbstractDatasetMapping,
    namesAutocompleteAnalyzer,
    namesAutocompleteSearchAnalyzer,
    ukrainianAddressesStopwordsAnalyzer,
)
from elasticsearch_dsl import DocType, Index

SMIDA_REPORT_INDEX = "ragoogle_smida_report"
smida_report_idx = Index(SMIDA_REPORT_INDEX)
smida_report_idx.settings(**BASIC_INDEX_SETTINGS)


smida_report_idx.analyzer(namesAutocompleteAnalyzer)
smida_report_idx.analyzer(namesAutocompleteSearchAnalyzer)
smida_report_idx.analyzer(ukrainianAddressesStopwordsAnalyzer)


@smida_report_idx.doc_type
class ElasticSmidaReportModel(AbstractDatasetMapping):
    def render_infocard(self):
        from .apps import SmidaReportConfig as AppConfig

        return render_to_string(
            "smida_reports/infocard.html",
            {
                "res": self,
                "url": self.get_absolute_url(),
                "datasource_name": AppConfig.name,
                "datasource_verbose_name": AppConfig.verbose_name,
            },
        )

    def external_url(self):
        if (getattr(self.report_title, "NREG", "") or "").lower() == "true":
            return "https://stockmarket.gov.ua/db/xml/news/{}/show".format(
                self.report_id
            )
        else:
            if relativedelta(
                dt_parse(self.report_title["FID"]), dt_parse(self.report_title["STD"])
            ).months > 4:
                return "https://stockmarket.gov.ua/db/xml/yearreports/{}/show".format(
                    self.report_id
                )
            else:
                return "https://stockmarket.gov.ua/db/xml/kvreports/{}/show".format(
                    self.report_id
                )

    def get_absolute_url(self):
        return reverse("smida_report>details", kwargs={"pk": self._id})

    class Meta:
        index = SMIDA_REPORT_INDEX
        doc_type = "ragoogle_smida_report_doctype"
