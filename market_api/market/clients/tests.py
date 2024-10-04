import json
import pytest

from copy import deepcopy
from django.core.handlers.wsgi import WSGIRequest
from rest_framework import status
from rest_framework.test import APIClient

from .models import Customer

from market.utils import random_numbers

@pytest.mark.django_db
def test_get_customers(
    api_client: APIClient, 
    customer: Customer, 
    customer_data: dict,
):
    
    # Act
    url: str = "/customers/"
    response: WSGIRequest = api_client.get(url, format="json")
    content: dict = json.loads(response.content)

    print("A" * 50)
    print(type(response))
    print("A" * 50)

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert content == {
        "Customers": [customer_data]
    }

@pytest.mark.django_db
def test_create_customer(
    api_client: APIClient, 
    customer_data: dict, 
):
    
    # Arrange
    new_customer: dict = deepcopy(customer_data)
    new_customer["id"] = 2
    new_customer["phone"] = ""
    new_customer["document"] = random_numbers()

    # Act
    url: str = "/customers/"
    response: WSGIRequest = api_client.post(
        url, 
        data=new_customer, 
        format="json",
    )
    content: dict = json.loads(response.content)

    # Assert
    assert response.status_code == status.HTTP_201_CREATED
    assert content == new_customer

@pytest.mark.django_db
def test_create_customer_with_empty_data(
    api_client: APIClient,
):
    
    # Arrange
    new_customer: dict = {}

    # Act
    url: str = "/customers/"
    response: WSGIRequest = api_client.post(
        url, 
        data=new_customer, 
        format="json",
    )
    content: dict = json.loads(response.content)

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert content == {
        "document": ["This field is required.",],
        "name": ["This field is required.",],
    }

@pytest.mark.django_db
def test_create_customer_without_document(
    api_client: APIClient, 
    customer_data: dict, 
):
    
    # Arrange
    new_customer: dict = deepcopy(customer_data)
    del new_customer["document"]

    # Act
    url: str = "/customers/"
    response: WSGIRequest = api_client.post(
        url, 
        data=new_customer, 
        format="json",
    )
    content: dict = json.loads(response.content)

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert content == {
        "document": ["This field is required.",],
    }

@pytest.mark.django_db
def test_create_customer_without_name(
    api_client: APIClient, 
    customer_data: dict, 
):
    
    # Arrange
    new_customer: dict = deepcopy(customer_data)
    new_customer["document"] = random_numbers()
    del new_customer["name"]

    # Act
    url: str = "/customers/"
    response: WSGIRequest = api_client.post(
        url, 
        data=new_customer, 
        format="json",
    )
    content: dict = json.loads(response.content)

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert content == {
        "name": ["This field is required.",],
    }

@pytest.mark.django_db
def test_get_customer(
    api_client: APIClient, 
    customer: Customer,
    customer_data: dict, 
):
    
    # Act
    url: str = f"/customers/{customer.pk}/"
    response: WSGIRequest = api_client.get(url, format="json")
    content: dict = json.loads(response.content)

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert content == customer_data

@pytest.mark.django_db
def test_get_not_found_customer(
    api_client: APIClient,
    customer_not_found: dict,
):
    
    # Act
    url: str = f"/customers/104/"
    response: WSGIRequest = api_client.get(url, format="json")
    content: dict = json.loads(response.content)

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert content == customer_not_found

@pytest.mark.django_db
def test_update_customer(
    api_client: APIClient, 
    customer_data: dict, 
):
    
    # Arrange
    customer_updated: dict = deepcopy(customer_data)
    customer_updated["phone"] = ""
    customer_updated["document"] = random_numbers()

    # Act
    id: int = customer_data["id"]
    url: str = f"/customers/{id}/"
    response: WSGIRequest = api_client.put(
        url, 
        data=customer_updated, 
        format="json",
    )
    content: dict = json.loads(response.content)

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert content == customer_updated

@pytest.mark.django_db
def test_delete_customer(
    api_client: APIClient, 
    customer: Customer,
    customer_deleted_message: dict,
):

    # Act
    url: str = f"/customers/{customer.pk}/"
    response: WSGIRequest = api_client.delete(url, format="json")

    # Assert
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.data == customer_deleted_message

@pytest.mark.django_db
def test_delete_not_found_customer(
    api_client: APIClient, 
    customer: Customer,
):

    # Act
    url: str = f"/customers/1233/"
    response: WSGIRequest = api_client.delete(url, format="json")

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND

