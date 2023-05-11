import csv
import sys

from django.apps import apps
from django.core.management.base import BaseCommand
from django.conf import settings
from users.models import User
from reviews.models import (Genre,
                            Category,
                            Title,
                            GenreTitle,
                            Review,
                            Comment)


CSV_PATH = f'{settings.STATICFILES_DIRS[0]}/data/'

models_to_load = (
    (Genre, 'genre.csv'),
    (Category, 'category.csv'),
    (User, 'users.csv'),
    (Title, 'titles.csv'),
    (Review, 'review.csv'),
    (Comment, 'comments.csv')
)

related_models_to_load = (
    (GenreTitle, 'genre_title.csv', {'title_id': Title, 'genre_id': Genre}),
)


class Command(BaseCommand):
    help = 'Creating model objects according the file path specified'

    def load_model(self, model, file, fields={}):
        sys.stdout.write(f'Загружаем {model.__name__}...')
        with open(file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            objs = []
            for row in reader:
                for field, rmodel in fields.items():
                    row[field] = rmodel.objects.get(pk=row[field])
                objs.append(model(**row))
            model.objects.bulk_create(objs)
        sys.stdout.write(self.style.SUCCESS('\t\t[OK]\n'))

    def handle(self, *args, **kwargs):
        for model, file in models_to_load:
            self.load_model(model, CSV_PATH + file)
        for model, file, fields in related_models_to_load:
            self.load_model(model, CSV_PATH + file, fields)
