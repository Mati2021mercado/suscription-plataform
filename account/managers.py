from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy


# MODIFICO EL METODO POR DEFECTO DE AUTHENTICACION
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, *args, **extra_fields):
        if not email:
            raise ValueError(gettext_lazy("Debe introducirse un email valido"))
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    def create_superuser(self,email,password,*args, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        
        if extra_fields.get("is_staff") is not True:
            raise ValueError(gettext_lazy("El superuser debe tener is_staff=True"))
        
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(gettext_lazy("El superuser debe tener is_superuser=True"))
        return self.create_user(email, password, **extra_fields)
        