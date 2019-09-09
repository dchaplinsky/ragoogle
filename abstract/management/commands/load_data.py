from django.core.management.base import BaseCommand, CommandError
from django.apps import apps as django_apps
from search.search_tools import get_apps_with_loader


class Command(BaseCommand):
    help = "Universal loader for the datasets"

    def add_arguments(self, parser):
        subparsers = parser.add_subparsers(
            dest="datasource", help="Invididual data sources"
        )

        for app_label in get_apps_with_loader():
            config = django_apps.app_configs[app_label]

            if hasattr(config, "loader_class"):
                loader = config.loader_class()
                subp = subparsers.add_parser(
                    name=app_label, help="{} dataset".format(config.verbose_name)
                )
                loader.inject_params(subp)

    def handle(self, *args, **options):
        loader = django_apps.app_configs[options["datasource"]].loader_class()

        loader.handle_details(*args, **options)
