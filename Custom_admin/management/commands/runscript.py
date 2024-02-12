from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Run a custom script in the context of a Django project'

    def add_arguments(self, parser):
        parser.add_argument('script_name', type=str)

    def handle(self, *args, **options):
        script_name = options['script_name']
        call_command(script_name, *args)
