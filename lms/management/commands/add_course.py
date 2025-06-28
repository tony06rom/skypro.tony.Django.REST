from django.core.management.base import BaseCommand
from django.core.management import call_command
from lms.models import Course


class Command(BaseCommand):

    def handle(self, *args, **options):
        Course.objects.all().delete()
        call_command('loaddata', 'fixtures/course_fixture.json')
        self.stdout.write(self.style.SUCCESS('Курсы загружены'))
