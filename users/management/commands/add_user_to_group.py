from django.contrib.auth.models import Group
from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        moderator = Group.objects.get(name="moderators")
        users_id = input('Пользователи (id) через запятую, которых вы хотите добавить в группу "модераторы":')
        users_id = users_id.split(",")
        for id in users_id:
            user = User.objects.get(id=id)
            user.groups.add(moderator)
        print("Пользователи добавлены в группу модераторов")
