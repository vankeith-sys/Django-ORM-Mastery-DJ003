from django.apps import AppConfig


class StudentsConfig(AppConfig):
    name = 'student'

    def ready(self):
        from . import signals
        # connecting apps.py to the signals file
