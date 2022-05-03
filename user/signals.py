from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Code,CustomUser


@receiver(post_save,sender = CustomUser)
def pos_save_generator_code(sender,instance,created,*args,**kwargs):
    if created:
        Code.objects.create(user=instance)