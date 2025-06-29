from django.core.management import call_command
from django.core.management.base import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        User.objects.all().delete()
        call_command("loaddata", "fixtures/user_fixture.json")
        self.stdout.write(self.style.SUCCESS("Пользователи добавлены"))
