import pytest

from employees.models import Employee

@pytest.mark.django_db
def test_employee_str(
    employee_data: dict,
    employee: Employee,
):

    # Arrange
    name: str = employee_data["name"]
    document: str = employee_data["document"]

    # Act
    employee_str: str = f"{employee}"

    # Assert
    assert type(employee_str) == str
    assert employee_str == f"{name} ({document})"
