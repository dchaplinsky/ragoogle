from elasticsearch_dsl.response import Response
from elasticsearch_dsl.utils import AttrDict, AttrList, ObjectBase

from django.http import JsonResponse


def serialize_for_api(data):
    """Transform complex types that we use into simple ones recursively.
    Note: recursion isn't followed when we know that transformed types aren't
    supposed to contain any more complex types.

    TODO: this is rather ugly, would look better if views/models defined
    transformations explicitly. This is hard to achieve with function-based
    views, so it's pending a CBV move."""

    if hasattr(data, "to_api"):
        return serialize_for_api(data.to_api())
    elif isinstance(data, Response):
        return serialize_for_api(data.hits._l_)
    elif isinstance(data, (AttrDict, ObjectBase)):
        res = data.to_dict()
        for f in ['names_autocomplete', 'hl']:
            if f in res:
                del res[f]

        if hasattr(data, "meta"):
            res["source"] = data.__class__.__name__
            res["id"] = data.meta.id
        return res
    elif isinstance(data, AttrList):
        return data._l_
    elif isinstance(data, dict):
        return {k: serialize_for_api(v) for k, v in data.items()}
    elif isinstance(data, (list, tuple, set)):
        return list(map(lambda x: serialize_for_api(x), data))
    return data
