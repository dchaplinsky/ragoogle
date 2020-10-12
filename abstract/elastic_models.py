from elasticsearch_dsl import (
    DocType,
    Text,
    Index,
    analyzer,
    tokenizer,
    token_filter,
    Date,
)

from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string

namesAutocompleteAnalyzer = analyzer(
    "namesAutocompleteAnalyzer",
    tokenizer=tokenizer(
        "autocompleteTokenizer",
        type="edge_ngram",
        min_gram=1,
        max_gram=25,
        token_chars=["letter", "digit"],
    ),
    filter=["lowercase"],
)

namesAutocompleteSearchAnalyzer = analyzer(
    "namesAutocompleteSearchAnalyzer",
    tokenizer=tokenizer("whitespace"),

    filter=[
        "lowercase"
    ]
)

ukrainianAddressesStopwordsAnalyzer = analyzer(
    "ukrainianAddressesStopwordsAnalyzer",
    type="ukrainian",
    filter=[
        token_filter(
            "addresses_stopwords",
            type="stop",
            stopwords=[
                _("будинок"),
                _("обл"),
                _("район"),
                _("вулиця"),
                _("місто"),
                _("м"),
                _("квартира"),
                _("вул"),
                _("село"),
                _("буд"),
                _("кв"),
                _("проспект"),
                _("область"),
                _("селище"),
                _("міського"),
                _("типу"),
                _("офіс"),
                _("н"),
                _("р"),
                _("б"),
                _("с"),
                _("провулок"),
                _("корпус"),
                _("бульвар"),
                _("кімната"),
                _("шосе"),
                _("в"),
                _("смт"),
                _("просп"),
                _("№"),
            ],
        ),
        "lowercase",
    ],
)

BASIC_INDEX_SETTINGS = {
    "number_of_shards": settings.NUM_THREADS,
    "number_of_replicas": 0,
}


class AbstractDatasetMapping(DocType):
    last_updated_from_dataset = Date()
    first_updated_from_dataset = Date()
    addresses = Text(analyzer="ukrainianAddressesStopwordsAnalyzer", copy_to="all")
    persons = Text(analyzer="ukrainian", copy_to="all")
    countries = Text(analyzer="ukrainian", copy_to="all")
    companies = Text(analyzer="ukrainian", copy_to="all")
    raw_records = Text(analyzer="ukrainian", copy_to="all")
    names_autocomplete = Text(
        analyzer="namesAutocompleteAnalyzer",
        search_analyzer="namesAutocompleteSearchAnalyzer",
        fields={"raw": Text(index=True)},
        term_vector="with_positions_offsets"
    )

    all = Text(analyzer="ukrainian")

    def render_infocard(self):
        return render_to_string("abstract/base_infocard.html", {"res": self})
