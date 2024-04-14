from django.contrib import admin

from .models import CustomUser, Staff

admin.site.register(CustomUser)
admin.site.register(Staff)