from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = 'Create superuser'

    def handle(self, *args, **options):
        superusers = User.objects.filter(is_superuser=True)
        if not superusers:
            username = 'admin'
            email = 'admin@admin.ru'
            password = '11111'
            User.objects.create_superuser(username=username,
                                          email=email,
                                          password=password)
            print(f'! ! Superuser created: username - {username}, '
                  f'email - {email}, password - {password} ! !')
        else:
            print('Superuser already exists')
