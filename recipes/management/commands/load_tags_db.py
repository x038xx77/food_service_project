from django.core.management import execute_from_command_line
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    @staticmethod
    def load_tags():
        execute_from_command_line(
            ['manage.py', 'loaddata', 'static/tags.json'])

    def handle(self, *args, **options):
        self.load_tags()
