from tqdm import tqdm

from django.core.management.base import BaseCommand
from django.db.models import Q

from src.actions.models import AnalyzedImage


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        to_optimize = AnalyzedImage.objects.filter(Q(optimized_image=None) | Q(optimized_image=''))

        print('Optimizing {} images'.format(to_optimize.count()))
        for img in tqdm(to_optimize):
            img.optimize_image()
            img.save()
