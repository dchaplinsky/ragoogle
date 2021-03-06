import os.path
import re
import argparse
from csv import DictReader, Sniffer, excel

from glob2 import iglob
from abstract.loaders import FileLoader
from abstract.tools.address_parser import PyJsHoisted_getAddress_ as get_address


class LetsPartyLoader(FileLoader):
    filetype = "csv"
    csv_dialect = excel
    last_updated_path = "donation_date"

    RCPT_MAPPING = {}

    remove_locality = [
        re.compile(r"^{}\s(.*)$".format(re.escape(r)), re.I)
        for r in ("селище міського типу", "село", "селище", "місто")
    ]

    @staticmethod
    def replace_aposthrophes(s):
        return s.replace("ʼ", "'").replace("`", "'").replace("’", "'")

    @classmethod
    def find_city_in_amice_parser(cls, amice_parser_data):
        amice_parser_data = {k.to_py(): amice_parser_data[k].to_py() for k in amice_parser_data}
        city = amice_parser_data.get("locality")
        if city is None:
            return None

        for r in cls.remove_locality:
            m = r.search(city)
            if m:
                return m.group(1).lower()

        return city.lower()


    def parse_city(self, address):
        address = self.replace_aposthrophes(address).lower()

        if address in self.parsed_cities_cache:
            return self.parsed_cities_cache[address]

        city = self.find_city_in_amice_parser(get_address(address))
        if not city:
            for loc in self.localities:
                m = re.search(loc, address)
                if m:
                    self.parsed_cities_cache[address] = m.group(1).lower()
                    return m.group(1).lower()

            self.parsed_cities_cache[address] = None
        else:
            self.parsed_cities_cache[address] = city
            return city


    def __init__(self, *args, **kwargs):
        self.localities = []
        self.parsed_cities_cache = {}

        fname = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "data/localities_fixed.txt",
        )

        with open(fname, "r") as fp:
            for l in fp:
                self.localities.append(
                    re.compile(r"\b({})\b".format(re.escape(l.strip())))
                )

        return super().__init__(*args, **kwargs)

    @property
    def model(self):
        from .models import LetsPartyModel

        return LetsPartyModel

    def inject_params(self, parser):
        parser.add_argument(
            "type",
            choices=self.model.TYPES.keys(),
            help="Type of dataset being imported",
        )

        parser.add_argument("filemask", help="Glob2 filemask to find files")

        parser.add_argument("--period", help="Period for report")
        parser.add_argument(
            "--last_updated_from_dataset",
            help="The date of the export of the dataset",
            required=self.last_updated_param_is_required,
        )

        parser.add_argument(
            "--store_broken_to",
            help="Store records that cannot be properly parsed into a file",
            type=argparse.FileType("w", encoding=self.encoding),
        )

    def preprocess(self, record, options):
        mapping = {
            "Дата надходження внеску": "donation_date",
            "Код платника (ЄДРПОУ)": "donator_code",
            "Місцезнаходження платника": "donator_location",
            "Найменування платника": "donator_name",
            "Партія": "party",
            "Сума (грн)": "amount",
            "Тип внескодавця": "donator_type",
            "ПІБ кандидата": "candidate_name",
            "Ідентифікаційний код (для фіз. осіб)/Код ЄДРПОУ (для юр. осіб)": "donator_code",
            "Місце проживання (для фіз. осіб)/Юридична адреса (для юр. осіб)": "donator_location",
            "ПІБ (для фіз. осіб)/Назва (для юр. осіб)": "donator_name",
            "Номер розрахункового документа": "transaction_doc_number",
            "Номер розрахункового документу": "transaction_doc_number",
            "Географічний обʼєкт": "geo",
            "Географічний об’єкт": "geo",
            "Вид рахунку": "account_type",
            "Квартал": "quarter",
            "Код ЄДРПОУ осередку": "branch_code",
            "Місцева організація": "branch_name",
            "Найменування банку": "bank_name",
            "Номер рахунку": "account_number",
            "Призначення (для спонсорських внесків)": "payment_subject",
            "Рік": "year",
            "Примітки": "notes",
            "type": "type",
            "Column": "",
        }

        record["type"] = options["type"]
        if None in record:
            print(record)

        record = {mapping[k]: v for k, v in record.items() if mapping[k]}
        if options["type"] == "nacp":
            if record["quarter"] == "5":
                record["period"] = "Річний звіт за {}".format(record["year"])
            else:
                record["period"] = "Звіт за {} квартал {}".format(
                    record["quarter"], record["year"]
                )
        else:
            record["period"] = options["period"]

        return record

    def get_ultimate_recepient(self, item):
        if item["type"] == "nacp":
            rcpt = item["party"]
        if item["type"] == "parliament":
            rcpt = item["party"]
        if item["type"] == "president":
            rcpt = item["candidate_name"]

        return self.RCPT_MAPPING.get(rcpt, rcpt)

    def get_payload_for_create(self, item, doc_hash, **kwargs):
        params = super().get_payload_for_create(item, doc_hash, **kwargs)
        year = 2019

        m = re.search(r"(\d{4})", item["period"])
        if m:
            year = int(m.group(1))

        params.update(
            {
                "type": item["type"],
                "period": item["period"],
                "year": year,
                "city": self.parse_city(item["donator_location"]),
                "amount": item["amount"].replace(",", "."),
                "ultimate_recepient": self.get_ultimate_recepient(item),
            }
        )

        return params

    def get_payload_for_update(self, item, doc_hash, **kwargs):
        return self.get_payload_for_create(item, doc_hash, **kwargs)

    def iter_dataset(self, options):
        for fname in iglob(options["filemask"]):
            with open(fname, "r", encoding=self.encoding) as fp:
                if self.csv_dialect is None:
                    dialect = Sniffer().sniff(fp.read(1024 * 16))
                    fp.seek(0)
                else:
                    dialect = self.csv_dialect

                r = DictReader(fp, dialect=dialect)
                for l in r:
                    l["type"] = options["type"]
                    yield l

    def get_dedup_fields(self):
        return [
            "donation_date",
            "donator_code",
            "donator_location",
            "donator_name",
            "party",
            "amount",
            "donator_type",
            "candidate_name",
            "transaction_doc_number",
            "geo",
            "account_type",
            "quarter",
            "branch_code",
            "branch_name",
            "bank_name",
            "account_number",
            "payment_subject",
            "year",
        ]
