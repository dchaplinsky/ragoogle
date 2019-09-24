import os
from datetime import date
from csv import DictReader

from django.core.management.base import BaseCommand, CommandError

from tqdm import tqdm
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse as parse_dt

from abstract.tools.companies import generate_edrpou_options
from lets_party.models import LetsPartyRedFlag, LetsPartyModel
from procurement_winners.elastic_models import ElasticProcurementWinnersModel
from tax_debts.elastic_models import ElasticTaxDebtsModel
from edrdr.elastic_models import ElasticEDRDRModel
from elasticsearch_dsl import Q
from jinja2_env import curformat, date_filter


def load_banks():
    fname = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "../../data/true_banks.csv"
    )

    res = set()
    with open(fname, "r") as fp:
        r = DictReader(fp)
        for l in r:
            res.add(int(l["edrpou"]))

    return res


class AbstractFlag:
    rule = "abstract_flag"
    entity_source = "abstract_entity"
    flag_type = "violation"
    banks = load_banks()

    def __init__(self):
        self.cache = {}

    def get_search(self, donation):
        raise NotImplementedError()

    def get_description(self, res, donation):
        raise NotImplementedError()

    def parse_code(self, code):
        try:
            code = int(code.strip().strip("\u200e"))
            if code in self.banks:
                return None
            else:
                return code

        except ValueError as e:
            print(code, e)
            return None

    def check_timebounds(self, donation_date, found_rec):
        if self.minus_delta is not None or self.plus_delta is not None:
            if hasattr(found_rec, "first_updated_from_dataset"):
                from_dt = found_rec.first_updated_from_dataset
            else:
                from_dt = found_rec.last_updated_from_dataset

            if self.minus_delta is not None:
                from_dt -= self.minus_delta

            to_dt = found_rec.last_updated_from_dataset
            if self.plus_delta is not None:
                to_dt += self.plus_delta

            return from_dt.date() <= donation_date.date() <= to_dt.date()

        return True

    def process(self, qs):
        for donation in tqdm(qs.iterator(), total=qs.count()):
            search_res = self.get_search(donation.data)
            if search_res is not None:
                filtered_res = []

                donation_date = parse_dt(donation.data["donation_date"])

                for res in search_res:
                    if self.check_timebounds(donation_date, res):
                        filtered_res.append(res)

                if filtered_res:
                    yield LetsPartyRedFlag(
                        flag_type=self.flag_type,
                        transaction=donation,
                        rule=self.rule,
                        related_entity=filtered_res[0]._id,
                        related_entity_source=self.entity_source,
                        description=self.get_description(filtered_res, donation),
                        payload=[debt.to_dict() for debt in filtered_res],
                    )


class CompanyWonProcurementFlag(AbstractFlag):
    rule = "company_won_procurement"
    entity_source = "procurement_winners"
    minus_delta = relativedelta(years=1)
    plus_delta = relativedelta(years=1)

    def get_search(self, donation):
        donator_code = self.parse_code(donation["donator_code"])
        if donator_code is None:
            return None

        if donator_code not in self.cache:
            search_res = (
                ElasticProcurementWinnersModel.search()
                .filter(
                    "terms", seller__code=list(generate_edrpou_options(donator_code))
                )
                .sort("-date")[:200]
                .execute()
            )
            self.cache[donator_code] = search_res
        else:
            search_res = self.cache[donator_code]

        return search_res

    def get_description(self, res, donation):
        return "Компанія перемогла на {} тендерах на загальну суму в {} грн".format(
            len(res), curformat(sum(r.volume_uah for r in res))
        )


class AbstractEDRDRFlag(AbstractFlag):
    rule = "abstract_edrdr"
    entity_source = "edrdr"
    edrdr_flag = "abstract_edrdr_flag"
    minus_delta = None
    plus_delta = None

    def search_clause(self, donator_code):
        return (
            ElasticEDRDRModel.search()
            .filter("terms", full_edrpou=list(generate_edrpou_options(donator_code)))
            .filter("term", **{self.edrdr_flag: True})[:200]
            .execute()
        )

    def get_search(self, donation):
        donator_code = self.parse_code(donation["donator_code"])
        if donator_code is None:
            return None

        if donator_code not in self.cache:
            search_res = self.search_clause(donator_code)
            self.cache[donator_code] = search_res
        else:
            search_res = self.cache[donator_code]

        return search_res


class CompanyIsHighRiskFlag(AbstractEDRDRFlag):
    rule = "company_is_high_risk"
    edrdr_flag = "internals__flags__has_high_risk"
    flag_type = "suspicious"

    def get_description(self, res, donation):
        return "Компанія має ознаки фіктивності"


class CompanyHasBOChangesFlag(AbstractEDRDRFlag):
    rule = "company_has_bo_changes"
    edrdr_flag = "internals__flags__bo_changes_dates"
    flag_type = "suspicious"
    change_minus_delta = relativedelta(weeks=2)
    change_plus_delta = relativedelta(weeks=1)

    def get_search(self, donation):
        donator_code = self.parse_code(donation["donator_code"])
        if donator_code is None:
            return None

        donation_date = parse_dt(donation["donation_date"]).date()

        search_res = (
            ElasticEDRDRModel.search()
            .filter("terms", full_edrpou=list(generate_edrpou_options(donator_code)))
            .query(
                "range",
                **{
                    self.edrdr_flag: {
                        "gte": donation_date - self.change_minus_delta,
                        "lte": donation_date + self.change_plus_delta,
                    }
                },
            )
            .execute()
        )

        return search_res

    def get_description(self, res, donation):
        donation_date = parse_dt(donation.data["donation_date"]).date()

        dates = set()
        for r in res:
            dates |= set(map(lambda x: parse_dt(x), getattr(r.internals.flags, "bo_changes_dates", [])))

        from_dt = donation_date - self.change_minus_delta
        to_dt = donation_date + self.change_plus_delta


        dates = list(filter(lambda x: from_dt <= x.date() <= to_dt, dates))

        return "Структура власності змінилася {}".format(", ".join(map(date_filter, sorted(dates))))


class CompanyHasForeignBOFlag(AbstractEDRDRFlag):
    rule = "company_has_foreign_bo"

    def search_clause(self, donator_code):
        return (
            ElasticEDRDRModel.search()
            .filter("terms", full_edrpou=list(generate_edrpou_options(donator_code)))
            .query(
                "bool",
                filter=[
                    Q("term", internals__flags__has_foreign_bo=True)
                    | Q("term", internals__flags__has_foreign_founders=True)
                ],
            )
            .execute()
        )

    def get_description(self, res, donation):
        countries = set()
        for r in res:
            countries |= set(getattr(r.internals.flags, "all_bo_countries", []))

        return "Компанія має закордоних бенефіціарних власників чи засновників з таких країн: {}".format(
            ", ".join(countries - set(["україна"]))
        )


class CompanyHasRussianBOFlag(AbstractEDRDRFlag):
    rule = "company_has_russian_bo"

    def search_clause(self, donator_code):
        return (
            ElasticEDRDRModel.search()
            .filter("terms", full_edrpou=list(generate_edrpou_options(donator_code)))
            .query(
                "bool",
                filter=[
                    Q("term", internals__flags__has_russian_bo=True)
                    | Q("term", internals__flags__has_russian_founders=True)
                ],
            )
            .execute()
        )

    def get_description(self, res, donation):
        return "Компанія має власників чи засновників з Росії"


class CompanyHasOccupiedBOFlag(AbstractEDRDRFlag):
    rule = "company_has_occupied_bo"

    def search_clause(self, donator_code):
        return (
            ElasticEDRDRModel.search()
            .filter("terms", full_edrpou=list(generate_edrpou_options(donator_code)))
            .query(
                "bool",
                filter=[
                    Q("term", internals__flags__has_bo_on_occupied_soil=True)
                    | Q("term", internals__flags__has_founders_on_occupied_soil=True)
                ],
            )
            .execute()
        )

    def get_description(self, res, donation):
        return "Компанія має власників чи засновників з ОРДЛО"


class CompanyHasCrimeaBOFlag(AbstractEDRDRFlag):
    rule = "company_has_crimea_bo"

    def search_clause(self, donator_code):
        return (
            ElasticEDRDRModel.search()
            .filter("terms", full_edrpou=list(generate_edrpou_options(donator_code)))
            .query(
                "bool",
                filter=[
                    Q("term", internals__flags__has_bo_in_crimea=True)
                    | Q("term", internals__flags__has_founders_in_crimea=True)
                ],
            )
            .execute()
        )

    def get_description(self, res, donation):
        return "Компанія має власників чи засновників з окупованого Криму"


class CompanyHasPEPBOFlag(AbstractEDRDRFlag):
    rule = "company_has_pep_bo"
    edrdr_flag = ""
    flag_type = "suspicious"

    def search_clause(self, donator_code):
        return (
            ElasticEDRDRModel.search()
            .filter("terms", full_edrpou=list(generate_edrpou_options(donator_code)))
            .query(
                "bool",
                filter=[
                    Q("term", internals__flags__has_pep_owner=True)
                    | Q("term", internals__flags__has_pep_founder=True)
                    | Q("term", internals__flags__had_pep_founder_in_the_past=True)
                    | Q("term", internals__flags__had_pep_owner_in_the_past=True)
                ],
            )
            .execute()
        )

    def get_description(self, res, donation):
        return (
            "Компанія має власників чи засновників що відносяться до публічних діячів"
        )


class CompanyIsNotActiveBOFlag(AbstractEDRDRFlag):
    rule = "company_is_not_active"
    flag_type = "suspicious"

    def get_search(self, donation):
        donator_code = self.parse_code(donation["donator_code"])
        if donator_code is None:
            return None

        if donator_code not in self.cache:
            search_res = (
                ElasticEDRDRModel.search()
                .filter(
                    "terms", full_edrpou=list(generate_edrpou_options(donator_code))
                )
                .exclude("term", latest_record__status="зареєстровано")
                .exclude("term", full_edrpou=20055032)  # ДКСУ
                .execute()
            )
            self.cache[donator_code] = search_res
        else:
            search_res = self.cache[donator_code]

        return search_res

    def get_description(self, res, donation):
        return 'Компанія має стан "{}"'.format(res[0].latest_record.status)


class CompanyHadTaxDebtsFlag(AbstractFlag):
    rule = "company_had_tax_debts"
    entity_source = "tax_debts"
    minus_delta = relativedelta(months=3)
    plus_delta = relativedelta(months=3)

    def get_search(self, donation):
        donator_code = self.parse_code(donation["donator_code"])
        if donator_code is None:
            return None

        if donator_code not in self.cache:
            search_res = (
                ElasticTaxDebtsModel.search()
                .filter("terms", TIN_S=list(generate_edrpou_options(donator_code)))
                .sort("-first_updated_from_dataset")[:200]
                .execute()
            )

            self.cache[donator_code] = search_res
        else:
            search_res = self.cache[donator_code]

        return search_res

    def get_description(self, res, donation):
        return "Компанія мала податковий борг на загальну суму в {} грн".format(
            curformat(max(debt["SUM_D"] + debt["SUM_M"] for debt in res) * 1000)
        )


class Command(BaseCommand):
    help = "Calculate redflags for party finances"
    RULES = [
        CompanyWonProcurementFlag,
        CompanyHadTaxDebtsFlag,
        CompanyHasForeignBOFlag,
        CompanyIsHighRiskFlag,
        CompanyIsNotActiveBOFlag,
        CompanyHasPEPBOFlag,
        CompanyHasRussianBOFlag,
        CompanyHasOccupiedBOFlag,
        CompanyHasCrimeaBOFlag,
        CompanyHasBOChangesFlag,
    ]

    def add_arguments(self, parser):
        parser.add_argument(
            "--drop_existing_flags",
            action="store_true",
            dest="drop_existing_flags",
            default=False,
            help="Delete existing flags before reindex",
        )

        parser.add_argument("--only_rule", choices=LetsPartyRedFlag.RULES.keys())

    def handle(self, *args, **options):
        if options["drop_existing_flags"]:
            qs = LetsPartyRedFlag.objects.all()

            if options["only_rule"]:
                qs = qs.filter(rule=options["only_rule"])

            qs.delete()

        all_donations = LetsPartyModel.objects.exclude(
            data__donator_type__in=[
                "гроші партії",
                "гроші кандидата",
                "державний бюджет",
            ]
        )
        company_donations = all_donations.exclude(data__donator_code="")
        person_donations = all_donations.filter(data__donator_code="")
        all_rules = {
            rule.rule: rule()
            for rule in self.RULES
            if (rule.rule == options["only_rule"] if options["only_rule"] else True)
        }

        flags_to_create = []
        for rule_name, rule in tqdm(all_rules.items()):
            qs = all_donations
            if rule_name.startswith("company_"):
                qs = company_donations
            elif rule_name.startswith("person_"):
                qs = person_donations

            flags_to_create += list(rule.process(qs))

        LetsPartyRedFlag.objects.bulk_create(flags_to_create)
