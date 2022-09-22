import random

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

#
from authentication.views import grant_permissions
from myFinance.models import Tag, Transaction


class Command(BaseCommand):
	#
	def add_arguments(self, parser):
		"""
		Entry point for subclassed commands to add custom arguments.
		"""
		pass

	def handle(self, *args, **options):
		user = User.objects.get(username='try_me')
		efraim = User.objects.get(username='efraim')
		# grant_permissions(user)
		Tag.objects.filter(user=user).delete()

		for tag in Tag.objects.filter(user=efraim):
			print("creating tag {}".format(tag.name))
			t = Tag.objects.create(user=user, name=tag.name, expense=tag.expense)
			count = 0
			for transaction in list(tag.transaction_set.all()):
				transaction.pk = transaction.id = None
				transaction.user = user
				transaction.tag = t # TODO may not work because tag was changed to FK
				transaction.value = transaction.value * (0.5 + random.uniform(0., 1.))
				transaction.save()
				count += 1
			print("createed {} transactions")

#         tag = Tag.objects.get(name=options['tag'][0])
#         tag_names = TagDb(TAG_DB_DIR).get_tagged_lists()[tag.file_name]
#         for t in tag_names:
#             for transaction in Transaction.objects.filter(name=t):
#                 transaction.tag = tag.name
#                 transaction.save()
