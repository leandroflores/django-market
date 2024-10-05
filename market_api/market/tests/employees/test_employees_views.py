import pytest

from employees.models import Employee
from employees.serializers import EmployeeSerializer
from employees.views import EmployeeAPIView

def test_model_name():

    # Arrange
    view: EmployeeAPIView = EmployeeAPIView()

    # Act
    model_name: str = view.model_name()

    # Assert
    assert model_name == "Employee"

def test_get_model():

    # Arrange
    view: EmployeeAPIView = EmployeeAPIView()

    # Act
    model: Employee = view.get_model()

    # Assert
    assert model == Employee

def test_get_serializer():

    # Arrange
    view: EmployeeAPIView = EmployeeAPIView()

    # Act
    serializer: EmployeeSerializer = view.get_serializer()

    # Assert
    assert serializer == EmployeeSerializer

@pytest.mark.django_db
def test_list_model(
    employee: Employee
):

    # Arrange
    view: EmployeeAPIView = EmployeeAPIView()

    # Act
    employees: list[Employee] = view.list_model()

    # Assert
    assert len(employees) == 1
    assert employees[0] == employee
