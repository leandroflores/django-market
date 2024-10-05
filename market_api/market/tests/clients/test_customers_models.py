import pytest

from clients.models import Customer

@pytest.mark.django_db
def test_customer_str(
    customer_data: dict,
    customer: Customer,
):

    # Arrange
    name: str = customer_data["name"]
    document: str = customer_data["document"]

    # Act
    customer_str: str = f"{customer}"

    # Assert
    assert type(customer_str) == str
    assert customer_str == f"{name} ({document})"
