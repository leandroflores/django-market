import pytest

from products.models import Category, Product
from products.serializers import CategorySerializer, ProductSerializer
from products.views import CategoryAPIView, ProductAPIView

def test_category_model_name():

    # Arrange
    view: CategoryAPIView = CategoryAPIView()

    # Act
    model_name: str = view.model_name()

    # Assert
    assert model_name == "Category"

def test_category_get_model():

    # Arrange
    view: CategoryAPIView = CategoryAPIView()

    # Act
    model: Category = view.get_model()

    # Assert
    assert model == Category

def test_category_get_serializer():

    # Arrange
    view: CategoryAPIView = CategoryAPIView()

    # Act
    serializer: CategorySerializer = view.get_serializer()

    # Assert
    assert serializer == CategorySerializer

@pytest.mark.django_db
def test_category_list_model(
    category: Category
):

    # Arrange
    view: CategoryAPIView = CategoryAPIView()

    # Act
    categories: list[Category] = view.list_model()

    # Assert
    assert len(categories) == 1
    assert categories[0] == category


def test_product_model_name():

    # Arrange
    view: ProductAPIView = ProductAPIView()

    # Act
    model_name: str = view.model_name()

    # Assert
    assert model_name == "Product"

def test_product_get_model():

    # Arrange
    view: ProductAPIView = ProductAPIView()

    # Act
    model: Product = view.get_model()

    # Assert
    assert model == Product

def test_product_get_serializer():

    # Arrange
    view: ProductAPIView = ProductAPIView()

    # Act
    serializer: ProductSerializer = view.get_serializer()

    # Assert
    assert serializer == ProductSerializer

@pytest.mark.django_db
def test_product_list_model(
    product: Product
):

    # Arrange
    view: ProductAPIView = ProductAPIView()

    # Act
    products: list[Product] = view.list_model()

    # Assert
    assert len(products) == 1
    assert products[0] == product
