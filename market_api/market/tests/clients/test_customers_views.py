import pytest

from clients.models import Customer
from clients.serializers import CustomerSerializer
from clients.views import CustomerAPIView

def test_model_name():

    # Arrange
    view: CustomerAPIView = CustomerAPIView()

    # Act
    model_name: str = view.model_name()

    # Assert
    assert model_name == "Customer"

def test_get_model():

    # Arrange
    view: CustomerAPIView = CustomerAPIView()

    # Act
    model: Customer = view.get_model()

    # Assert
    assert model == Customer

def test_get_serializer():

    # Arrange
    view: CustomerAPIView = CustomerAPIView()

    # Act
    serializer: CustomerSerializer = view.get_serializer()

    # Assert
    assert serializer == CustomerSerializer

@pytest.mark.django_db
def test_list_model(
    customer: Customer
):

    # Arrange
    view: CustomerAPIView = CustomerAPIView()

    # Act
    customers: list[Customer] = view.list_model()

    # Assert
    assert len(customers) == 1
    assert customers[0] == customer
