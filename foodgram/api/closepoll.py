from django.core.management.base import BaseCommand, CommandError
from recipe.models import Unit


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('ingredients_unit', nargs='+', type=str)

    def handle(self, *args, **options):
        for poll_id in options['ingredients_unit']:
            try:
                poll = Poll.objects.get(pk=ingredients_unit)
            except Unit.DoesNotExist:
                raise CommandError('Poll "%s" does not exist' % poll_id)

            poll.opened = False
            poll.save()

            self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"' % poll_id))