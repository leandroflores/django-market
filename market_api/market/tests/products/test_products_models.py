import pytest

from products.models import Category, Product

@pytest.mark.django_db
def test_category_str(
    category_data: dict,
    category: Category,
):

    # Arrange
    name: str = category_data["name"]

    # Act
    category_str: str = f"{category}"

    # Assert
    assert type(category_str) == str
    assert category_str == f"{name}"


@pytest.mark.django_db
def test_product_str(
    product_data: dict,
    product: Product,
):

    # Arrange
    name: str = product_data["name"]

    # Act
    product_str: str = f"{product}"

    # Assert
    assert type(product_str) == str
    assert product_str == f"{name}"
