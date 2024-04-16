from django.db import models

from useraccount.models import CustomUser

class Folder(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(CustomUser, related_name='folders', on_delete=models.CASCADE)
    parent_folder = models.ForeignKey('self', related_name='sub_folders', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

class File(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(CustomUser, related_name='files', on_delete=models.CASCADE)
    folder = models.ForeignKey(Folder, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='files/')
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']


class FilePermission(models.Model):
    user = models.ForeignKey(CustomUser, related_name='file_permissions', on_delete=models.CASCADE, db_column='user_id')
    file = models.ForeignKey(File, related_name='permissions', on_delete=models.CASCADE, db_column='file_id')
    can_view = models.BooleanField(default=False)
    can_edit = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['file', 'user']


class FolderPermission(models.Model):
    user = models.ForeignKey(CustomUser, related_name='folder_permissions', on_delete=models.CASCADE, db_column='user_id')
    folder = models.ForeignKey(Folder, related_name='permissions', on_delete=models.CASCADE, db_column='folder_id')
    can_view = models.BooleanField(default=False)
    can_edit = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['folder', 'user']

