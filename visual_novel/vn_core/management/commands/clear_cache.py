from django.core.cache import caches
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        caches["default"].clear()
