from collections import defaultdict
from decimal import Decimal

from django.shortcuts import render
from django.http import Http404
from django.db.models import Count, Sum, Max, Subquery
from django.views.generic import TemplateView

from elasticsearch.exceptions import NotFoundError

from .elastic_models import ElasticLetsPartyModel
from .models import LetsPartyModel, LetsPartyRedFlag
from .apps import LetsPartyConfig as DataSourceConfig


class LetsPartyDetailsView(TemplateView):
    template_name = "lets_party/details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            rec = ElasticLetsPartyModel.get(id=kwargs["pk"])
        except NotFoundError:
            raise Http404("Записа не існує")

        context["rec"] = rec
        context["datasource"] = DataSourceConfig

        return context


class LetsPartyHomeView(TemplateView):
    template_name = "lets_party/landing.html"

    def merge_breakdowns(
        self, total_breakdown, violation_breakdown, suspicious_breakdown
    ):
        def struct():
            return {
                "violation": {
                    "by_date": defaultdict(lambda: {"cnt": 0, "amount": Decimal()}),
                    "total_cnt": 0,
                    "total_amount": Decimal(),
                },
                "suspicious": {
                    "by_date": defaultdict(lambda: {"cnt": 0, "amount": Decimal()}),
                    "total_cnt": 0,
                    "total_amount": Decimal(),
                },
                "total": {
                    "by_date": defaultdict(lambda: {"cnt": 0, "amount": Decimal()}),
                    "total_cnt": 0,
                    "total_amount": Decimal(),
                },
            }

        merged_breakdown = defaultdict(struct)

        for k, breakdown in {
            "total": total_breakdown,
            "violation": violation_breakdown,
            "suspicious": suspicious_breakdown,
        }.items():
            for stats in breakdown:
                merged_breakdown[stats["ultimate_recepient"]][k]["total_cnt"] += stats[
                    "cnt"
                ]
                merged_breakdown[stats["ultimate_recepient"]][k][
                    "total_amount"
                ] += stats["amount"]

                merged_breakdown[stats["ultimate_recepient"]][k]["by_date"][
                    stats["period"]
                ]["cnt"] += stats["cnt"]
                merged_breakdown[stats["ultimate_recepient"]][k]["by_date"][
                    stats["period"]
                ]["amount"] += stats["amount"]

        return merged_breakdown

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        qs = LetsPartyModel.objects.exclude(
            data__donator_type__in=[
                "гроші партії",
                "гроші кандидата",
                "державний бюджет",
            ]
        )

        violation_qs = qs.filter(
            pk__in=Subquery(
                LetsPartyRedFlag.objects.filter(flag_type="violation").values(
                    "transaction_id"
                )
            )
        )
        suspicious_qs = qs.filter(
            pk__in=Subquery(
                LetsPartyRedFlag.objects.filter(flag_type="suspicious").values(
                    "transaction_id"
                )
            )
        )

        total_qs = qs.filter(
            pk__in=Subquery(LetsPartyRedFlag.objects.values("transaction_id"))
        )

        stats = qs.aggregate(
            transactions_cnt=Count("pk"),
            transactions_sum=Sum("amount"),
            transactions_max=Max("amount"),
        )

        stats_violation = violation_qs.aggregate(
            violation_cnt=Count("pk"), violation_sum=Sum("amount")
        )

        stats_suspicious = suspicious_qs.aggregate(
            suspicious_cnt=Count("pk"), suspicious_sum=Sum("amount")
        )

        stats_total = total_qs.aggregate(total_cnt=Count("pk"), total_sum=Sum("amount"))

        context.update(stats)
        context.update(stats_violation)
        context.update(stats_suspicious)
        context.update(stats_total)
        context.update(
            {
                "violation_transactions_cnt": LetsPartyRedFlag.objects.filter(
                    flag_type="violation"
                ).count(),
                "suspicious_transactions_cnt": LetsPartyRedFlag.objects.filter(
                    flag_type="suspicious"
                ).count(),
                "violation_rcpt_cnt": violation_qs.values("ultimate_recepient")
                .distinct()
                .count(),
                "suspicious_rcpt_cnt": suspicious_qs.values("ultimate_recepient")
                .distinct()
                .count(),
                "total_transactions_cnt": LetsPartyRedFlag.objects.count(),
                "total_rcpt_cnt": violation_qs.values("ultimate_recepient")
                .distinct()
                .count(),
            }
        )

        violation_breakdown = (
            violation_qs.values("ultimate_recepient", "period")
            .annotate(amount=Sum("amount"), cnt=Count("pk"))
            .filter(cnt__gte=0)
        )
        suspicious_breakdown = (
            suspicious_qs.values("ultimate_recepient", "period")
            .annotate(amount=Sum("amount"), cnt=Count("pk"))
            .filter(cnt__gte=0)
        )

        total_breakdown = (
            total_qs.values("ultimate_recepient", "period")
            .annotate(amount=Sum("amount"), cnt=Count("pk"))
            .filter(cnt__gte=0)
        )

        context["breakdown"] = self.merge_breakdowns(
            total_breakdown, violation_breakdown, suspicious_breakdown
        )

        return context


class LetsPartyRedFlagsView(TemplateView):
    template_name = "lets_party/redflags.html"

    def get_context_data(self, ultimate_recepient, period=None, **kwargs):
        context = super().get_context_data(**kwargs)

        qs = LetsPartyModel.objects.filter(
            ultimate_recepient=ultimate_recepient
        ).exclude(
            data__donator_type__in=[
                "гроші партії",
                "гроші кандидата",
                "державний бюджет",
            ]
        ).prefetch_related("flags")

        if period is not None:
            qs = qs.filter(period=period)

        qs = (
            qs.annotate(flags_cnt=Count("flags__pk"))
            .order_by("-flags_cnt")
            .exclude(flags_cnt=0)
        )


        if qs.count() == 0:
            raise Http404("Записа не існує")

        context.update({
            "transactions": qs,
            "ultimate_recepient": ultimate_recepient,
            "period": period
        })

        return context
