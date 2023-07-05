import json

from django.core.management.base import BaseCommand
from ..models import Country


def add_children(current_country, children):
    for child in children:
        print(child)
        child_country = Country.objects.create(name=child['name'], tn_parent=current_country)
        if child.get('children'):
            add_children(child_country, child['children'])


class Command(BaseCommand):
    help = 'Upload countries from json file'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        Country.objects.all().delete()
        with open('place/management/fixtures/iraq.json', encoding='utf-8') as f:
            self.handle_categories(f)
        with open('place/management/fixtures/turkey.json', encoding='utf-8') as f:
            self.handle_categories(f)
        with open('place/management/fixtures/iran.json', encoding='utf-8') as f:
            self.handle_categories(f)
        with open('place/management/fixtures/syria.json', encoding='utf-8') as f:
            self.handle_categories(f)
        with open('place/management/fixtures/egypt.json', encoding='utf-8') as f:
            self.handle_categories(f)
        with open('place/management/fixtures/lebanon.json', encoding='utf-8') as f:
            self.handle_categories(f)
        with open('place/management/fixtures/uae.json', encoding='utf-8') as f:
            self.handle_categories(f)
        with open('place/management/fixtures/tunisia.json', encoding='utf-8') as f:
            self.handle_categories(f)
        with open('place/management/fixtures/ksa.json', encoding='utf-8') as f:
            self.handle_categories(f)
        with open('place/management/fixtures/malaysia.json', encoding='utf-8') as f:
            self.handle_categories(f)

    def handle_categories(self, f):
        categories = json.load(f)
        current = Country.objects.create(name=categories['name'])
        add_children(current, categories['children'])
