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


