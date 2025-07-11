from django.core.management.base import BaseCommand
from main.models import Destination
from django.db import models

class Command(BaseCommand):
    help = "Supprime toutes les destinations sans hébergements."

    def handle(self, *args, **kwargs):
        to_delete = Destination.objects.annotate(nb_hebergements=models.Count('hebergements')).filter(nb_hebergements=0)
        count = to_delete.count()
        to_delete.delete()
        self.stdout.write(self.style.SUCCESS(f"{count} destinations sans hébergements supprimées.")) 