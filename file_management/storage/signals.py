from django.db.models.signals import post_save
from django.dispatch import receiver

from useraccount.models import CustomUser

from .models import Folder

@receiver(post_save, sender=CustomUser)
def create_user_root_folder(sender, instance, created, **kwargs):
    if created:
        
        Folder.objects.create(name='Root', owner=instance)