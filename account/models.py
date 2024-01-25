from django.db import models
from . managers import CustomUserManager
# Create your models here.

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
# AbstractBaseUser es una clase abstracta que se usa para crear user models personalizados con authenticacion personalizada y permisos
# PermissionsMixin es una clase abstracta que añade fields y varios metodos que se pueden usar para manejar grupos de usuarios o usuarios
from django.utils.timezone import now

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username=None
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=135)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=now)
    is_writer = models.BooleanField(default=True, verbose_name="Are you a writer?")
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()
    
    def __str__(self):
        return self.email
    