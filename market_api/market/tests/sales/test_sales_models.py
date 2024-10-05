import pytest

from clients.models import Customer
from products.models import Product
from sales.models import Sale, SaleItem

@pytest.mark.django_db
def test_sale_str(
    sale_data: dict,
    customer: Customer,
    sale: Sale,
):

    # Arrange
    id: str = str(sale_data["id"])
    date: str = str(sale_data["date"])

    # Act
    sale_str: str = f"{sale}"

    # Assert
    assert type(sale_str) == str
    assert sale_str == f"Sale {id} - {date} - {customer}"


@pytest.mark.django_db
def test_sale_item_str(
    sale_item_values: dict,
    product: Product,
    sale: Sale,
):

    # Arrange
    item: SaleItem = SaleItem(**sale_item_values)
    item.sale = sale
    item.product = product
    item.save()

    quantity: int = sale_item_values["quantity"]
    unit_price: float = sale_item_values["unit_price"]
    total_price: float = sale_item_values["total_price"]

    # Act
    item_str: str = f"{item}"

    # Assert
    assert type(item_str) == str
    assert item_str == f"{product} {quantity} x {unit_price} = {total_price}"
