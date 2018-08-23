from elasticsearch_dsl import DocType, Index
from django.template.loader import render_to_string


PAPER_DECLARATION_INDEX = "declarations_v2"
paper_declaration_idx = Index(PAPER_DECLARATION_INDEX)


@paper_declaration_idx.doc_type
class ElasticPaperDeclarationModel(DocType):
    def render_infocard(self):
        from .apps import PaperDeclarationsConfig as AppConfig

        return render_to_string(
            "paper_declarations/infocard.html",
            {
                "res": self,
                "url": "https://declarations.com.ua/declaration/{}".format(self.meta.id),
                "datasource_name": AppConfig.name,
                "datasource_verbose_name": AppConfig.verbose_name,
            },
        )

    class Meta:
        index = PAPER_DECLARATION_INDEX
        doc_type = "declaration"
