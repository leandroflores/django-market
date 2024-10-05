import pytest

from sales.models import Sale
from sales.serializers import SaleSerializer
from sales.views import SaleAPIView

def test_model_name():

    # Arrange
    view: SaleAPIView = SaleAPIView()

    # Act
    model_name: str = view.model_name()

    # Assert
    assert model_name == "Sale"

def test_get_model():

    # Arrange
    view: SaleAPIView = SaleAPIView()

    # Act
    model: Sale = view.get_model()

    # Assert
    assert model == Sale

def test_get_serializer():

    # Arrange
    view: SaleAPIView = SaleAPIView()

    # Act
    serializer: SaleSerializer = view.get_serializer()

    # Assert
    assert serializer == SaleSerializer

@pytest.mark.django_db
def test_list_model(
    sale: Sale
):

    # Arrange
    view: SaleAPIView = SaleAPIView()

    # Act
    sales: list[Sale] = view.list_model()

    # Assert
    assert len(sales) == 1
    assert sales[0] == sale
