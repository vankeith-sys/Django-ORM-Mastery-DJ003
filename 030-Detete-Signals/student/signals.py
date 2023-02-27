from django.db.models.signals import (
    pre_delete,
    post_delete,
    pre_save,
    post_save,
)
from .models import Student
from django.dispatch import receiver

@receiver(pre_delete, sender=Student)
def pre_delete(sender, **kwargs):
    print('You are about to delete sumn')

@receiver(post_delete, sender=Student)
def post_delete(sender, **kwargs):
    print('You just deleted a student or sumn')

@receiver(pre_save, sender=Student)
def pre_save(sender, instance: Student, **kwargs):
    print('******** START PRE SAVE ********')
    print(instance)
    print(type(instance))
    print('******** END PRE SAVE ********')
