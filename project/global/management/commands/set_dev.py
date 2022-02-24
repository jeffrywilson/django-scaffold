from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site


class Command(BaseCommand):
    help = "Set site to dev"

    def handle(self, *args, **kwargs):
        self.stdout.write("Setting site to dev.example.com")
        mysite = Site.objects.get(pk=1)
        mysite.name = "dev"
        mysite.domain = "dev.example.com"
        mysite.save()
