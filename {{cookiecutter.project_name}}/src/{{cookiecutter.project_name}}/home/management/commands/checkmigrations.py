from collections import defaultdict

from django.conf import settings
from django.core.management.base import CommandError
from django.core.management.commands.makemigrations import Command as MakeMigrations
from django.db.migrations.loader import MigrationLoader

from {{cookiecutter.project_name}}.lib.utils import hash_migrations


class Command(MakeMigrations):
    help = "Check if migrations are as expected"  # noqa: A003

    def add_arguments(self, parser):
        pass

    @staticmethod
    def check_hashes():
        actual_hashes = hash_migrations()
        with open(settings.MIGRATION_HASHES_PATH) as file:
            saved_hashes = [line.strip() for line in file.readlines()]
        if actual_hashes != saved_hashes:
            raise CommandError("Migration hashes have changed!")

    @staticmethod
    def check_naming():
        loader = MigrationLoader(None, ignore_no_migrations=True)
        nodes = loader.graph.nodes
        app_migrations = defaultdict(list)
        for node in nodes:
            try:
                migration_number = int(node[1].lstrip("0").split("_")[0])
            except (IndexError, ValueError) as exc:
                raise CommandError(f"Migration {node[1]} has an invalid name") from exc
            app_migrations[node[0]].append(migration_number)

        for app_name, migration_numbers in app_migrations.items():
            n = len(migration_numbers)
            if len(set(migration_numbers)) != n:
                raise CommandError(f"Two migrations in {app_name} have the same prefix")
            migration_numbers.sort()
            if migration_numbers[-1] != n:
                raise CommandError(f"There is a skipped prefix in {app_name}")

    def handle(self, *args, **options):
        options["check_changes"] = True
        options["dry_run"] = True
        options["interactive"] = False
        options["merge"] = False
        options["empty"] = False
        options["name"] = ""
        options["include_header"] = False
        super().handle(*args, **options)
        self.check_naming()
        self.check_hashes()