import json

from redis.exceptions import ConnectionError

from django.core.cache import cache
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Load genres from given json file to cache'

    def add_arguments(self, parser):
        parser.add_argument('genres_file', nargs='+', type=str)

    def handle(self, *args, **options):
        genres_file = options['genres_file'][0]
        try: 
            with open(genres_file) as f:
                for genre, artists in json.load(f).items():
                    cache.set(genre, artists, None)
        except FileNotFoundError as e:
            raise CommandError(f'{genres_file}: File does not exist')
        except ConnectionError as e:
            raise CommandError(f'Cannot reach REDIS. Please check connection')

        self.stdout.write(self.style.SUCCESS(f'Successfully load genres file {genres_file}'))
