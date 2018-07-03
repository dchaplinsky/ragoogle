from elasticsearch_dsl import DocType, Index
from django.template.loader import render_to_string


GARNAHATA_INDEX = "garnahata_ownerships"
garnahata_idx = Index(GARNAHATA_INDEX)


@garnahata_idx.doc_type
class ElasticGarnahataModel(DocType):
    def render_infocard(self):
        from .apps import GarnahataInUaConfig as AppConfig

        return render_to_string(
            "garnahata_in_ua/infocard.html",
            {
                "res": self,
                "url": "https://garnahata.in.ua{}".format(self.url),
                "datasource_name": AppConfig.name,
                "datasource_verbose_name": AppConfig.verbose_name,
            },
        )

    class Meta:
        index = GARNAHATA_INDEX
        doc_type = "garnahata_ownerships_doctype"
