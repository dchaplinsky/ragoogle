from elasticsearch_dsl import DocType, Index
from django.template.loader import render_to_string


EDRDR_INDEX = "edrdr_companies"
edrdr_idx = Index(EDRDR_INDEX)


@edrdr_idx.doc_type
class ElasticEDRDRModel(DocType):
    def render_infocard(self):
        from .apps import EDRDRConfig as AppConfig

        return render_to_string(
            "edrdr/infocard.html",
            {
                "res": self,
                "url": "https://ring.org.ua/edr/uk/company/{}".format(self.full_edrpou),
                "datasource_name": AppConfig.name,
                "datasource_verbose_name": AppConfig.verbose_name,
            },
        )

    class Meta:
        index = EDRDR_INDEX
        doc_type = "edrdr_companies_doctype"
