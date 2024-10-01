from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

TYPE_CHOICES = [
    ("F", "Físico"),
    ("J", "Jurídico"),
]

class Client(models.Model):
    document = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=1, choices=TYPE_CHOICES, default="F")
    email = models.EmailField(blank=True)
    phone = PhoneNumberField(blank=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.name} ({self.document})"
