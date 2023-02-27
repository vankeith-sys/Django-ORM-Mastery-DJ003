from django.db.models.signal import pre_delete, post_delete
from .models import Student
from django.dispatch import receiver

@receiver(pre_delete, sender=Student)
def pre_delete(sender, **kwargs):
    print('You are about to delete sumn')

@receiver(post_delete, sender=Student)
def post_delete(ender, **kwargs):
    print('You just deleted a student or sumn')
