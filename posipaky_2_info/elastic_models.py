from elasticsearch_dsl import DocType, Index
from django.template.loader import render_to_string


MINIONS2_INDEX = "posiparium"
minions2_idx = Index(MINIONS2_INDEX)


@minions2_idx.doc_type
class ElasticMinion2Model(DocType):
    def render_infocard(self):
        from .apps import Posipaky2InfoConfig as AppConfig

        return render_to_string(
            "posipaky_2_info/infocard.html",
            {
                "res": self,
                "url": "https://posipaky-2.info/mp/{}".format(self.mp.id),
                "datasource_name": AppConfig.name,
                "datasource_verbose_name": AppConfig.verbose_name,
            },
        )

    class Meta:
        index = MINIONS2_INDEX
        doc_type = "posiparium_minions_doctype"
