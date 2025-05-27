from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.apps import apps

class Command(BaseCommand):
    help = 'Configura grupos e permissões iniciais'

    def handle(self, *args, **options):
        # Definição dos grupos
        grupos = {
            'ADMIN': {
                'perms': Permission.objects.all()
            },
            'MANAGER': {
                'perms': Permission.objects.filter(
                    codename__in=[
                        'add_users', 'change_users', 'view_users',
                        'add_componenttype', 'change_componenttype', 'view_componenttype',
                        'add_reservoir', 'change_reservoir', 'view_reservoir',
                    ]
                )
            },
            'OPERATOR': {
                'perms': Permission.objects.filter(
                    codename__in=[
                        'add_users', 'view_users',
                        'add_componenttype', 'view_componenttype',
                        'add_sensor', 'view_sensor',
                    ]
                )
            },
            'VIEWER': {
                'perms': Permission.objects.filter(
                    codename__startswith='view_'
                )
            },
        }

        for nome, info in grupos.items():
            grupo, criado = Group.objects.get_or_create(name=nome)
            grupo.permissions.set(info['perms'])
            self.stdout.write(self.style.SUCCESS(
                f"Grupo '{nome}' configurado com {info['perms'].count()} permissões."
            ))