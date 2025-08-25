from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_kitchen = models.BooleanField(default=False)
    is_delivery_agent = models.BooleanField(default=False)
    phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.username

    class Meta:
        db_table = "customuser"
    
    def get_details(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "phone": self.phone,
            "is_customer": self.is_customer,
            "is_kitchen": self.is_kitchen,
            "is_delivery_agent": self.is_delivery_agent,
        }