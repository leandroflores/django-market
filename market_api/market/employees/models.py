from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class Employee(models.Model):
    document = models.CharField(max_length=11, unique=True)
    name = models.CharField(max_length=100) 
    department = models.CharField(max_length=100, default="Sales")
    hire_date = models.DateField()
    phone = PhoneNumberField(blank=True)
    email = models.EmailField(blank=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.name} ({self.document})"
