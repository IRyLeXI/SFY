from django.core.management.base import BaseCommand
from django.db import transaction
from user.models import CustomUser
from user.models import create_default_playlists

class Command(BaseCommand):
    help = 'Create default playlists for existing users'

    def handle(self, *args, **kwargs):
        users = CustomUser.objects.all()
        self.stdout.write(f'Found {users.count()} users. Creating playlists...')
        with transaction.atomic():
            for user in users:
                create_default_playlists(CustomUser, user, created=True)
                self.stdout.write(f'Playlists created for user: {user.username}')
        self.stdout.write('Playlists creation for existing users completed.')
