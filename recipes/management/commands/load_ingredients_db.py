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
        ingredient_db = os.path.join(BASE_DIR, 'static', 'ingredients.json')
        with open(ingredient_db) as f:
            ingredients = json.load(f)
            for ingredient in ingredients:
                ingredient_obj, created = Ingredient.objects.get_or_create(
                    title=ingredient['title'],
                    dimension=ingredient['dimension'])
            msg = f'Successfully loaded {len(ingredients)} ingredients'
            self.stdout.write(self.style.SUCCESS(msg))

    def handle(self, *args, **options):
        self.load_ingredients()
