from django.db import models

from clients.models import Customer
from employees.models import Employee
from products.models import Product

PAYMENT_CHOICES = [
    ("DINHEIRO", "Dinheiro"),
    ("CHEQUE", "Cheque"),
    ("DEBITO", "Débito"),
    ("CREDITO", "Crédito"),
    ("PIX", "Pix"),
    ("VALE_ALIMENTACAO", "Vale Alimentação"),
]

STATUS_CHOICES = [
    ("PAGO", "Pago"),
    ("PENDENTE", "Pendente"),
    ("CANCELADO", "Cancelado"),
]

class Sale(models.Model):
    date = models.DateField()
    hour = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment = models.CharField(blank=True, null=True, max_length=30, choices=PAYMENT_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="sales")
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="sales")

    @staticmethod
    def columns_header() -> list:
        return [
            "Date", 
            "Hour", 
            "Customer",
            "Employee",
            "Status",
            "Payment",
            "Discount",
            "Total Amount",
        ]

    @property
    def row(self) -> list:
        return [
            self.date.strftime("%d/%m/%Y"),
            self.hour.strftime("%H:%M"),
            self.customer.name,
            self.employee.name,
            self.status,
            self.payment,
            f"{self.discount:.2f}",
            f"{self.total_amount:.2f}",
        ]

    def __str__(self):
        return f"Sale {self.pk} - {self.date} - {self.customer}"
    
class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

    def __str__(self):
        return f"{self.product} {self.quantity} x {self.unit_price} = {self.total_price}"
