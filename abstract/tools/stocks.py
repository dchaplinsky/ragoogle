import os.path
from csv import DictReader


def load_stock_types(fname):
    res = {}
    with open(fname, "r") as fp:
        r = DictReader(fp)
        for l in r:
            res[l["code"].lstrip("0")] = {k: v.strip() for k, v in l.items() if k != "code"}

    return res

STOCK_TYPES = load_stock_types(
    os.path.join(os.path.dirname(__file__), "gazetteers/stock_types.csv")
)
