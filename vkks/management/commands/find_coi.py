import sys
import argparse

from tqdm import tqdm
from time import sleep
from collections import defaultdict
import requests

from django.core.management.base import BaseCommand

from vkks.elastic_models import ElasticVKKSModel
from csv import DictWriter


class Command(BaseCommand):
    help = "Search for COI using CONP API"

    def add_arguments(self, parser):
        parser.add_argument(
            "--outfile", nargs="?", type=argparse.FileType("w"), default=sys.stdout
        )
        parser.add_argument(
            "--login",
        )
        parser.add_argument(
            "--password",
        )

    @staticmethod
    def get_id_name(lastname, firstname, patronymic):
        if "(" in lastname:
            lastname = lastname[0 : lastname.index("(")].strip()

        if not firstname:
            return None

        if patronymic:
            return f"{lastname} {firstname[0]}. {patronymic[0]}."
        else:
            return f"{lastname} {firstname[0]}."

    @staticmethod
    def search_lawsuits(judge, other, fieldname="attorney.idName"):
        return {
            "query": "-самовідвід",
            "defaultOperator": "and",
            "filter": {
                "judge.idName": {"list": [judge], "operator": "or"},
                fieldname: {"list": [other], "operator": "or"},
            },
            "sort": {},
            "searchIndex": "lawsuit",
            "from": 0,
            "aggregation": False,
        }

    @staticmethod
    def get_token(options):
        return requests.post(
            "https://api.conp.com.ua/api/v1.0/user/login",
            data={
                "email": options["login"],
                "password": options["password"]
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        ).json()

    def handle(self, *args, **options):
        qs = ElasticVKKSModel.search().query(
            "match", general__family__career__position={"query": "адвокат"}
        )

        token = self.get_token(options)

        writer = DictWriter(
            options["outfile"],
            fieldnames=[
                "case",
                "decisions",
                "judge",
                "counterpart",
                "counterpart_position",
                "date",
                "declaration_link",
            ],
        )
        writer.writeheader()

        found_cases = defaultdict(set)
        docs = []
        for rec in qs.scan():
            docs.append(rec)

        for i, doc in enumerate(tqdm(docs, total=qs.count())):
            if i and i % 600:
                try:
                    token = self.get_token(options)
                except Exception:
                    sleep(5)
                    token = self.get_token(options)

            judge = self.get_id_name(
                doc.general.last_name, doc.general.name, doc.general.patronymic
            )
            if not judge:
                self.stderr.write(
                    f"Cannot parse judge name {doc.general.last_name} {doc.general.name} {doc.general.patronymic}, skipping"
                )
                continue

            newly_added = []
            for fam in doc.general.family:
                if any(map(lambda x: "адвокат" in x["position"].lower(), fam.career)):
                    member = self.get_id_name(fam.last_name, fam.name, fam.patronymic)
                    if not member:
                        self.stderr.write(
                            f"Cannot parse family name {fam.last_name} {fam.name} {fam.patronymic}, skipping"
                        )
                        continue

                    q = self.search_lawsuits(
                        judge, member
                    )
                    resp = requests.post(
                        "https://api.conp.com.ua/api/v1.0/lawsuit/search",
                        headers={"Authorization": token},
                        json=q,
                    ).json()

                    if resp["total"]:
                        for case in resp["items"]:
                            if case["lawsuitNumber"] not in found_cases:
                                newly_added.append(
                                    {
                                        "case": case["lawsuitNumber"],
                                        "judge": f"{doc.general.last_name} {doc.general.name} {doc.general.patronymic}",
                                        "counterpart": f"{fam.last_name} {fam.name} {fam.patronymic}",
                                        "counterpart_position": "\n".join(
                                            f"{career['position']}, {career['workplace']}"
                                            for career in fam.career
                                        ),
                                        "date": case["lawsuitDate"],
                                        "declaration_link": "https://ring.org.ua{}".format(
                                            doc.get_absolute_url()
                                        ),
                                    }
                                )
                            found_cases[case["lawsuitNumber"]].add(case["id"])

            for added in newly_added:
                added["decisions"] = "\n".join(
                    f"https://conp.com.ua/lawsuit/{decision_id}"
                    for decision_id in found_cases[added["case"]]
                )

                writer.writerow(added)
