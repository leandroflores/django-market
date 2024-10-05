import json
import pytest

from copy import deepcopy
from django.core.handlers.wsgi import WSGIRequest
from rest_framework import status
from rest_framework.test import APIClient

from .models import Employee
from market.utils import random_numbers, random_str

@pytest.mark.django_db
def test_get_employees(
    api_client: APIClient, 
    employee_url: str,
    employee: Employee, 
    employee_data: dict,
):
    
    # Act
    url: str = f"{employee_url}/"
    response: WSGIRequest = api_client.get(url, format="json")
    content: dict = json.loads(response.content)

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert content == {
        "Employees": [employee_data]
    }

@pytest.mark.django_db
def test_create_employee(
    api_client: APIClient, 
    employee_url: str,
    employee_data: dict, 
):
    
    # Arrange
    new_employee: dict = deepcopy(employee_data)
    new_employee["id"] = 2
    new_employee["phone"] = ""
    new_employee["document"] = random_numbers()

    # Act
    url: str = f"{employee_url}/"
    response: WSGIRequest = api_client.post(
        url, 
        data=new_employee, 
        format="json",
    )
    content: dict = json.loads(response.content)

    # Assert
    assert response.status_code == status.HTTP_201_CREATED
    assert content == new_employee

@pytest.mark.django_db
def test_create_employee_with_empty_data(
    api_client: APIClient,
    employee_url: str,
):
    
    # Arrange
    new_employee: dict = {}

    # Act
    url: str = f"{employee_url}/"
    response: WSGIRequest = api_client.post(
        url, 
        data=new_employee, 
        format="json",
    )
    content: dict = json.loads(response.content)

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert content == {
        "document": ["This field is required.",],
        "name": ["This field is required.",],
        "hire_date": ["This field is required.",],
    }

@pytest.mark.django_db
def test_create_employee_without_document(
    api_client: APIClient, 
    employee_url: str,
    employee_data: dict, 
):
    
    # Arrange
    new_employee: dict = deepcopy(employee_data)
    del new_employee["document"]

    # Act
    url: str = f"{employee_url}/"
    response: WSGIRequest = api_client.post(
        url, 
        data=new_employee, 
        format="json",
    )
    content: dict = json.loads(response.content)

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert content == {
        "document": ["This field is required.",],
    }

@pytest.mark.django_db
def test_create_employee_with_invalid_document(
    api_client: APIClient, 
    employee_url: str,
    employee_data: dict, 
):
    
    # Arrange
    new_employee: dict = deepcopy(employee_data)
    new_employee["document"] = ""

    # Act
    url: str = f"{employee_url}/"
    response: WSGIRequest = api_client.post(
        url, 
        data=new_employee, 
        format="json",
    )
    content: dict = json.loads(response.content)

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert content == {
        "document": ["This field may not be blank.",],
    }

@pytest.mark.django_db
def test_create_employee_without_name(
    api_client: APIClient, 
    employee_url: str,
    employee_data: dict, 
):
    
    # Arrange
    new_employee: dict = deepcopy(employee_data)
    new_employee["document"] = random_numbers()
    del new_employee["name"]

    # Act
    url: str = f"{employee_url}/"
    response: WSGIRequest = api_client.post(
        url, 
        data=new_employee, 
        format="json",
    )
    content: dict = json.loads(response.content)

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert content == {
        "name": ["This field is required.",],
    }

@pytest.mark.django_db
def test_create_employee_with_invalid_name(
    api_client: APIClient, 
    employee_url: str,
    employee_data: dict, 
):
    
    # Arrange
    new_employee: dict = deepcopy(employee_data)
    new_employee["document"] = random_numbers()
    new_employee["name"] = ""

    # Act
    url: str = f"{employee_url}/"
    response: WSGIRequest = api_client.post(
        url, 
        data=new_employee, 
        format="json",
    )
    content: dict = json.loads(response.content)

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert content == {
        "name": ["This field may not be blank.",],
    }

@pytest.mark.django_db
def test_create_employee_with_invalid_email(
    api_client: APIClient, 
    employee_url: str,
    employee_data: dict, 
):
    
    # Arrange
    new_employee: dict = deepcopy(employee_data)
    new_employee["document"] = random_numbers()
    new_employee["email"] = random_str()

    # Act
    url: str = f"{employee_url}/"
    response: WSGIRequest = api_client.post(
        url, 
        data=new_employee, 
        format="json",
    )
    content: dict = json.loads(response.content)

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert content == {
        "email": ["Enter a valid email address.",],
    }

@pytest.mark.django_db
def test_create_employee_with_invalid_phone(
    api_client: APIClient, 
    employee_url: str,
    employee_data: dict, 
):
    
    # Arrange
    new_employee: dict = deepcopy(employee_data)
    new_employee["document"] = random_numbers()
    new_employee["phone"] = random_numbers()

    # Act
    url: str = f"{employee_url}/"
    response: WSGIRequest = api_client.post(
        url, 
        data=new_employee, 
        format="json",
    )
    content: dict = json.loads(response.content)

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert content == {
        "phone": ["The phone number entered is not valid.",],
    }

@pytest.mark.django_db
def test_get_employee(
    api_client: APIClient, 
    employee_url: str,
    employee: Employee,
    employee_data: dict, 
):
    
    # Act
    url: str = f"{employee_url}/{employee.pk}/"
    response: WSGIRequest = api_client.get(url, format="json")
    content: dict = json.loads(response.content)

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert content == employee_data

@pytest.mark.django_db
def test_get_not_found_employee(
    api_client: APIClient,
    employee_url: str,
    id_not_found: int,
    employee_not_found: dict,
):
    
    # Act
    url: str = f"{employee_url}/{id_not_found}/"
    response: WSGIRequest = api_client.get(url, format="json")
    content: dict = json.loads(response.content)

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert content == employee_not_found

@pytest.mark.django_db
def test_update_employee(
    api_client: APIClient, 
    employee_url: str, 
    employee_data: dict, 
):
    
    # Arrange
    employee_updated: dict = deepcopy(employee_data)
    employee_updated["phone"] = ""
    employee_updated["document"] = random_numbers()

    # Act
    id: int = employee_data["id"]
    url: str = f"{employee_url}/{id}/"
    response: WSGIRequest = api_client.put(
        url, 
        data=employee_updated, 
        format="json",
    )
    content: dict = json.loads(response.content)

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert content == employee_updated

@pytest.mark.django_db
def test_update_not_found_employee(
    api_client: APIClient, 
    employee_url: str,
    id_not_found: int,
    employee_data: dict, 
    employee_not_found: dict,
):
    
    # Arrange
    employee_updated: dict = deepcopy(employee_data)
    employee_updated["phone"] = ""
    employee_updated["document"] = random_numbers()

    # Act
    url: str = f"{employee_url}/{id_not_found}/"
    response: WSGIRequest = api_client.put(
        url, 
        data=employee_updated, 
        format="json",
    )
    content: dict = json.loads(response.content)

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert content == employee_not_found

@pytest.mark.django_db
def test_update_employee_without_document(
    api_client: APIClient, 
    employee_url: str,
    employee_data: dict, 
):
    
    # Arrange
    employee_updated: dict = deepcopy(employee_data)
    del employee_updated["document"]

    # Act
    id: int = employee_data["id"]
    url: str = f"{employee_url}/{id}/"
    response: WSGIRequest = api_client.put(
        url, 
        data=employee_updated, 
        format="json",
    )
    content: dict = json.loads(response.content)

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert content == {
        "document": ["This field is required.",],
    }

@pytest.mark.django_db
def test_delete_employee(
    api_client: APIClient, 
    employee_url: str,
    employee: Employee,
    employee_deleted_message: dict,
):

    # Act
    url: str = f"{employee_url}/{employee.pk}/"
    response: WSGIRequest = api_client.delete(url, format="json")

    # Assert
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.data == employee_deleted_message

@pytest.mark.django_db
def test_delete_not_found_employee(
    api_client: APIClient, 
    employee_url: str,
    id_not_found: int,
    employee: Employee,
    employee_not_found: dict,
):

    # Act
    url: str = f"{employee_url}/{id_not_found}/"
    response: WSGIRequest = api_client.delete(url, format="json")
    content: dict = json.loads(response.content)

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert content == employee_not_found

