import os.path
from csv import DictReader


def load_countries(fname):
    res = {}
    with open(fname, "r") as fp:
        r = DictReader(fp)
        for l in r:
            res[l["code"]] = {k: v.strip() for k, v in l.items() if k != "code"}

    return res

COUNTRIES = load_countries(
    os.path.join(os.path.dirname(__file__), "gazetteers/country_codes.csv")
)
