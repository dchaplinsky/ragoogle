from elasticsearch_dsl import DocType, Index
from django.template.loader import render_to_string


NACP_DECLARATION_INDEX = "nacp_declarations_new"
nacp_declaration_idx = Index(NACP_DECLARATION_INDEX)


@nacp_declaration_idx.doc_type
class ElasticNACPDeclarationModel(DocType):
    def render_infocard(self):
        from .apps import NACPDeclarationsConfig as AppConfig

        return render_to_string(
            "nacp_declarations/infocard.html",
            {
                "res": self,
                "url": "https://declarations.com.ua/declaration/{}".format(self.meta.id),
                "datasource_name": AppConfig.name,
                "datasource_verbose_name": AppConfig.verbose_name,
            },
        )

    class Meta:
        index = NACP_DECLARATION_INDEX
        doc_type = "nacp_declaration_doctype"
