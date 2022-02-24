from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings

class Command(BaseCommand):

	help = 'Sends a test email to specified input email, like "python3 manage.py testemail myemail@email.com"'

	def add_arguments(self, parser):
		parser.add_argument('email', type=str)

	def handle(self, *args, **options):
		email = options.get('email', None)
		send_mail(
			'Test Subject',
			'Test Message',
			settings.ADMINS,
			[email],
			fail_silently=False,
		)
		