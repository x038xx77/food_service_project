import json
import os

from django.core.management.base import BaseCommand

from recipes.models import Ingredient
from foodgram.settings import BASE_DIR
import logging
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Imports ingredients and tags to the DataBase'

    def load_ingredients(self):
        with open(os.path.join(
            BASE_DIR,
            'igredientdb',
            'ingredients.json')) as f: # noqa
            ingredients = json.load(f)
            for ingredient in ingredients:
                try:
                    ingredient_obj, created = Ingredient.objects.get_or_create(
                        title=ingredient['title'],
                        dimension=ingredient['dimension'])
                    if created:
                        msg = f'Successfully loaded \
                            {len(ingredients)} ingredients'
                        self.stdout.write(self.style.SUCCESS(msg))
                except Exception as e:
                    logger.error(str(e))

    def handle(self, *args, **options):
        self.load_ingredients()
