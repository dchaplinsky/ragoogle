from elasticsearch_dsl import DocType, Index
from django.template.loader import render_to_string


MINIONS_INDEX = "minions"
minions_idx = Index(MINIONS_INDEX)


@minions_idx.doc_type
class ElasticMinionModel(DocType):
    def render_infocard(self):
        from .apps import PosipakyInfoConfig as AppConfig

        return render_to_string(
            "posipaky_info/infocard.html",
            {
                "res": self,
                "url": "https://posipaky.info/mp/{}".format(self.mp.id),
                "datasource_name": AppConfig.name,
                "datasource_verbose_name": AppConfig.verbose_name,
            },
        )

    class Meta:
        index = MINIONS_INDEX
        doc_type = "minions_minions_doctype"
