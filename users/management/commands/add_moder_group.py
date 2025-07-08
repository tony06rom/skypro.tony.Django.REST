from django.contrib.auth.models import Group
from django.core.management import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        Group.objects.all().delete()
        moderator = Group.objects.create(name="moderators")
        moderator.save()
