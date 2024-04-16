from django.db.models.signals import post_save
from django.dispatch import receiver

from useraccount.models import CustomUser

from .models import Folder, File, FilePermission, FolderPermission

@receiver(post_save, sender=CustomUser)
def create_user_root_folder(sender, instance, created, **kwargs):
    if created:
        
        Folder.objects.create(name='Root', owner=instance)

@receiver(post_save, sender=Folder)
def update_folder_permission(sender, instance, created, **kwargs):
    if created:
        defaults = {
            'can_edit': True,
            'can_delete': True,
            "can_view": True
        }
        FolderPermission.objects.get_or_create(
            folder=instance,
            user=instance.owner,
            defaults=defaults
        )


@receiver(post_save, sender=File)
def update_file_permission(sender, instance, created, **kwargs):
    if created:
        defaults = {
            'can_edit': True,
            'can_delete': True,
            "can_view": True
        }
        FilePermission.objects.get_or_create(
            file=instance,
            user=instance.owner,
            defaults=defaults
        )
