from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site


class Command(BaseCommand):
    help = "Set site to django-scaffold.herokuapp.com"

    def handle(self, *args, **kwargs):
        self.stdout.write("Setting site to django-scaffold.herokuapp.com")
        project = Site.objects.get(pk=1)
        project.name = "Heroku Django Scaffold"
        project.domain = "django-scaffold.herokuapp.com"
        project.save()
