import os

from django.core.management.base import BaseCommand
from django.core.management.color import supports_color

from accounts.models import *


class Command(BaseCommand):
    help = 'Admins'

    @property
    def colors(self):
        b = supports_color() or os.environ.get('PYCHARM_HOSTED') or os.environ.get('PYCHARM_DJANGO_MANAGE_MODULE')
        return {
            'yellow': '\033[033m' if b else '',
            'reset': '\033[0m' if b else ''
        }

    def handle(self, *args, **options):

        data = [
            ('admin@amdin.admin', 'admin'),
            ('ceo@4-com.pro', 'Vitaliy V Antoshchenko'),
            ('revastanislav@gmail.com', 'Stas'),
            ('pljut098@gmail.com', 'test Testovich'),
            ('bublik_oleg@hotmail.com', 'Oleg'),
        ]

        for email, username in data:
            if not User.objects.filter(email=email).exists():
                u = User(
                    username=username,
                    email=email,
                    is_admin=True,
                    is_active=True,
                )
                u.set_password('qwerty123456')
                u.save()
                print(u)
