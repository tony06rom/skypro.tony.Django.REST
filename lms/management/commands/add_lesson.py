from django.core.management.base import BaseCommand
from django.core.management import call_command
from lms.models import Lesson


class Command(BaseCommand):

    def handle(self, *args, **options):
        Lesson.objects.all().delete()
        call_command('loaddata', 'fixtures/lesson_fixture.json')
        self.stdout.write(self.style.SUCCESS('Уроки загружены'))
