from django.db import models

# Create your models here.
from account.models import CustomUser

class Subscription(models.Model):
    
    subscriber_name = models.CharField(max_length=300)
    subscription_plan = models.CharField(max_length=255)
    subscription_cost = models.CharField(max_length=255)
    paypal_subscription_id = models.CharField(max_length=300)
    is_active = models.BooleanField(default=False)
    # Entonces, si tenemos una referencia a un usuario en el modelo de suscripción y ese usuario se elimina, ese usuario se eliminará del modelo de usuario personalizado y también del modelo de suscripción.
    # Unique= True porque es un usuario y una suscripcion
    user = models.OneToOneField(CustomUser,max_length=10, on_delete=models.CASCADE, unique=True)
    
    def __str__(self):
        return f'{self.subscriber_name} - {self.subscription_plan} subscription'