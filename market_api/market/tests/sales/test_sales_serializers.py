import pytest

from copy import deepcopy
from clients.models import Customer
from employees.models import Employee
from products.models import Product
from sales.models import Sale, SaleItem
from sales.serializers import SaleSerializer

@pytest.mark.django_db
def test_sale_serializer_create(
    sale_values: dict,
    customer: Customer,
    employee: Employee,
    product: Product,
):
    
    # Arrange
    sale_data: dict = deepcopy(sale_values)
    sale_data["customer"] = customer.pk
    sale_data["employee"] = employee.pk
    sale_data["items"] = [
        {
            "product": product.pk,
            "quantity": 2,
            "unit_price": 10.00,
            "total_price": 20.00,
        }
    ]
        
    # Act
    serializer: SaleSerializer = SaleSerializer(data=sale_data)
    assert serializer.is_valid(), serializer.errors
    sale: Sale = serializer.save()

    # Assert
    assert sale.customer == customer

@pytest.mark.django_db
def test_update_sale(
    sale_values: dict,
    sale_item_values: dict,
    customer: Customer,
    employee: Employee,
    product: Product,
):
    
    # Arrange
    sale: Sale = Sale(**sale_values)
    sale.customer = customer
    sale.employee = employee
    sale.save()
    
    item: SaleItem = SaleItem(**sale_item_values)
    item.sale = sale
    item.product = product
    item.save()

    # Act
    updated_total: float = 45.00
    updated_data: dict = deepcopy(sale_values)
    updated_data["customer"] = customer.pk
    updated_data["employee"] = employee.pk
    updated_data["total_amount"] = updated_total
    updated_data["items"] = [
        {
            "product": product.pk,
            "quantity": 3, 
            "unit_price": 15.00,
            "total_price": updated_total,
        }
    ]
    serializer: SaleSerializer = SaleSerializer(sale, data=updated_data)
    assert serializer.is_valid(), serializer.errors
    updated_sale: Sale = serializer.save()

    assert updated_sale.date == sale_values["date"]
    assert updated_sale.hour == sale_values["hour"]
    assert updated_sale.status == sale_values["status"]
    assert updated_sale.discount == sale_values["discount"]
    assert updated_sale.total_amount == updated_total
    assert updated_sale.payment == sale_values["payment"]

    assert SaleItem.objects.count() == 1
    new_item = SaleItem.objects.first()
    assert new_item.product == product
    assert new_item.quantity == 3
    assert new_item.unit_price == 15.00
    assert new_item.total_price == updated_total