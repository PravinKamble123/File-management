# models.py

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager

class CustomUserManager(UserManager):
    def _create_user(self, email, name, password, **extra_fields):
        if not email:
            raise ValueError("You have not specified a valid e-mail address")
    
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    def create_owner(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault('is_owner', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, name, password, **extra_fields)

    def create_staff(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault('is_owner', False)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, name, password, **extra_fields)

    def create_user(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault('is_owner', False)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(email, name, password, **extra_fields)
    def create_superuser(self, name=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(name, email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_owner = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        related_name='custom_users',
        related_query_name='custom_user'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        related_name='custom_users',
        related_query_name='custom_user'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

class Staff(models.Model):
    owner = models.ForeignKey(CustomUser, related_name='my_staff_members', on_delete=models.CASCADE)
    staff = models.ForeignKey(CustomUser, related_name='my_owners', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    update_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

