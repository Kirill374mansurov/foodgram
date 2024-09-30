from django.core import management
from django.core.management.base import BaseCommand


FILES = ['ingredients.csv',]


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        for csv_file in FILES:
            management.call_command('import_CSV', csv_file)
