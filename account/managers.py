from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy


# MODIFICO EL METODO POR DEFECTO DE AUTHENTICACION
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, args, **kwards):
        if not email:
            raise ValueError(gettext_lazy("Debe introducirse un email valido"))
        
        email = self.normalize_email(email)
        user = self.model(email=email, **kwards)
        user.set_password(password)
        user.save()
        return user