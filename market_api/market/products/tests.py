import json
import pytest

from copy import deepcopy
from django.core.handlers.wsgi import WSGIRequest
from rest_framework import status
from rest_framework.test import APIClient

from .models import Category, Product
from market.utils import random_numbers, random_str

@pytest.mark.django_db
def test_get_categories(
    api_client: APIClient, 
    category_url: str,
    category: Category, 
    category_data: dict,
):
    
    # Act
    url: str = f"{category_url}/"
    response: WSGIRequest = api_client.get(url, format="json")
    content: dict = json.loads(response.content)

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert content == {
        "Categories": [category_data]
    }

@pytest.mark.django_db
def test_create_category(
    api_client: APIClient, 
    category_url: str,
    category_data: dict, 
):
    
    # Arrange
    new_category: dict = deepcopy(category_data)
    new_category["id"] = 2
    new_category["name"] = random_str()

    # Act
    url: str = f"{category_url}/"
    response: WSGIRequest = api_client.post(
        url, 
        data=new_category, 
        format="json",
    )
    content: dict = json.loads(response.content)

    # Assert
    assert response.status_code == status.HTTP_201_CREATED
    assert content["id"] == new_category["id"]
    assert content["name"] == new_category["name"]
    assert content["description"] == new_category["description"]


@pytest.mark.django_db
def test_create_category_with_empty_data(
    api_client: APIClient,
    category_url: str,
):
    
    # Arrange
    new_category: dict = {}

    # Act
    url: str = f"{category_url}/"
    response: WSGIRequest = api_client.post(
        url, 
        data=new_category, 
        format="json",
    )
    content: dict = json.loads(response.content)

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert content == {
        "name": ["This field is required.",],
    }

@pytest.mark.django_db
def test_create_category_without_name(
    api_client: APIClient, 
    category_url: str,
    category_data: dict, 
):
    
    # Arrange
    new_category: dict = deepcopy(category_data)
    del new_category["name"]

    # Act
    url: str = f"{category_url}/"
    response: WSGIRequest = api_client.post(
        url, 
        data=new_category, 
        format="json",
    )
    content: dict = json.loads(response.content)

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert content == {
        "name": ["This field is required.",],
    }

@pytest.mark.django_db
def test_create_category_with_invalid_name(
    api_client: APIClient, 
    category_url: str,
    category_data: dict, 
):
    
    # Arrange
    new_category: dict = deepcopy(category_data)
    new_category["name"] = ""

    # Act
    url: str = f"{category_url}/"
    response: WSGIRequest = api_client.post(
        url, 
        data=new_category, 
        format="json",
    )
    content: dict = json.loads(response.content)

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert content == {
        "name": ["This field may not be blank.",],
    }

@pytest.mark.django_db
def test_get_category(
    api_client: APIClient, 
    category_url: str,
    category: Category,
    category_data: dict, 
):
    
    # Act
    url: str = f"{category_url}/{category.pk}/"
    response: WSGIRequest = api_client.get(url, format="json")
    content: dict = json.loads(response.content)

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert content == category_data

@pytest.mark.django_db
def test_get_not_found_category(
    api_client: APIClient,
    category_url: str,
    id_not_found: int,
    category_not_found: dict,
):
    
    # Act
    url: str = f"{category_url}/{id_not_found}/"
    response: WSGIRequest = api_client.get(url, format="json")
    content: dict = json.loads(response.content)

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert content == category_not_found

@pytest.mark.django_db
def test_update_category(
    api_client: APIClient, 
    category_url: str, 
    category_data: dict, 
):
    
    # Arrange
    category_updated: dict = deepcopy(category_data)
    category_updated["name"] = random_numbers()

    # Act
    id: int = category_data["id"]
    url: str = f"{category_url}/{id}/"
    response: WSGIRequest = api_client.put(
        url, 
        data=category_updated, 
        format="json",
    )
    content: dict = json.loads(response.content)

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert content == category_updated

@pytest.mark.django_db
def test_update_not_found_category(
    api_client: APIClient, 
    category_url: str,
    id_not_found: int,
    category_data: dict, 
    category_not_found: dict,
):
    
    # Arrange
    category_updated: dict = deepcopy(category_data)
    category_updated["name"] = random_numbers()

    # Act
    url: str = f"{category_url}/{id_not_found}/"
    response: WSGIRequest = api_client.put(
        url, 
        data=category_updated, 
        format="json",
    )
    content: dict = json.loads(response.content)

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert content == category_not_found

@pytest.mark.django_db
def test_delete_category(
    api_client: APIClient, 
    category_url: str,
    category: Category,
    category_deleted_message: dict,
):

    # Act
    url: str = f"{category_url}/{category.pk}/"
    response: WSGIRequest = api_client.delete(url, format="json")

    # Assert
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.data == category_deleted_message

@pytest.mark.django_db
def test_delete_not_found_category(
    api_client: APIClient, 
    category_url: str,
    id_not_found: int,
    category: Category,
    category_not_found: dict,
):

    # Act
    url: str = f"{category_url}/{id_not_found}/"
    response: WSGIRequest = api_client.delete(url, format="json")
    content: dict = json.loads(response.content)

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert content == category_not_found

@pytest.mark.django_db
def test_get_products(
    api_client: APIClient, 
    product_url: str,
    product: Product, 
    product_data: dict,
):
    
    # Act
    url: str = f"{product_url}/"
    response: WSGIRequest = api_client.get(url, format="json")
    content: dict = json.loads(response.content)

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert content == {
        "Products": [product_data]
    }

@pytest.mark.django_db
def test_create_product(
    api_client: APIClient, 
    product_url: str,
    product_data: dict, 
):
    
    # Arrange
    new_product: dict = deepcopy(product_data)
    new_product["id"] = 2
    new_product["name"] = random_str()

    # Act
    url: str = f"{product_url}/"
    response: WSGIRequest = api_client.post(
        url, 
        data=new_product, 
        format="json",
    )
    content: dict = json.loads(response.content)

    # Assert
    assert response.status_code == status.HTTP_201_CREATED
    assert content["id"] == new_product["id"]
    assert content["name"] == new_product["name"]
    assert content["description"] == new_product["description"]
    assert content["price"] == new_product["price"]
    assert content["stock"] == new_product["stock"]
    assert content["category"] == new_product["category"]

@pytest.mark.django_db
def test_create_product_with_empty_data(
    api_client: APIClient,
    product_url: str,
):
    
    # Arrange
    new_product: dict = {}

    # Act
    url: str = f"{product_url}/"
    response: WSGIRequest = api_client.post(
        url, 
        data=new_product, 
        format="json",
    )
    content: dict = json.loads(response.content)

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert content == {
        "name": ["This field is required.",],
        "price": ["This field is required.",],
        "stock": ["This field is required.",],
        "category": ["This field is required.",],
    }

@pytest.mark.django_db
def test_create_product_without_name(
    api_client: APIClient, 
    product_url: str,
    product_data: dict, 
):
    
    # Arrange
    new_product: dict = deepcopy(product_data)
    del new_product["name"]

    # Act
    url: str = f"{product_url}/"
    response: WSGIRequest = api_client.post(
        url, 
        data=new_product, 
        format="json",
    )
    content: dict = json.loads(response.content)

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert content == {
        "name": ["This field is required.",],
    }

@pytest.mark.django_db
def test_create_product_with_invalid_name(
    api_client: APIClient, 
    product_url: str,
    product_data: dict, 
):
    
    # Arrange
    new_product: dict = deepcopy(product_data)
    new_product["name"] = ""

    # Act
    url: str = f"{product_url}/"
    response: WSGIRequest = api_client.post(
        url, 
        data=new_product, 
        format="json",
    )
    content: dict = json.loads(response.content)

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert content == {
        "name": ["This field may not be blank.",],
    }

@pytest.mark.django_db
def test_create_product_without_price(
    api_client: APIClient, 
    product_url: str,
    product_data: dict, 
):
    
    # Arrange
    new_product: dict = deepcopy(product_data)
    del new_product["price"]

    # Act
    url: str = f"{product_url}/"
    response: WSGIRequest = api_client.post(
        url, 
        data=new_product, 
        format="json",
    )
    content: dict = json.loads(response.content)

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert content == {
        "price": ["This field is required.",],
    }

@pytest.mark.django_db
def test_create_product_with_invalid_price(
    api_client: APIClient, 
    product_url: str,
    product_data: dict, 
):
    
    # Arrange
    new_product: dict = deepcopy(product_data)
    new_product["price"] = ""

    # Act
    url: str = f"{product_url}/"
    response: WSGIRequest = api_client.post(
        url, 
        data=new_product, 
        format="json",
    )
    content: dict = json.loads(response.content)

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert content == {
        "price": ["A valid number is required.",],
    }

@pytest.mark.django_db
def test_create_product_without_stock(
    api_client: APIClient, 
    product_url: str,
    product_data: dict, 
):
    
    # Arrange
    new_product: dict = deepcopy(product_data)
    del new_product["stock"]

    # Act
    url: str = f"{product_url}/"
    response: WSGIRequest = api_client.post(
        url, 
        data=new_product, 
        format="json",
    )
    content: dict = json.loads(response.content)

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert content == {
        "stock": ["This field is required.",],
    }

@pytest.mark.django_db
def test_create_product_with_invalid_stock(
    api_client: APIClient, 
    product_url: str,
    product_data: dict, 
):
    
    # Arrange
    new_product: dict = deepcopy(product_data)
    new_product["stock"] = ""

    # Act
    url: str = f"{product_url}/"
    response: WSGIRequest = api_client.post(
        url, 
        data=new_product, 
        format="json",
    )
    content: dict = json.loads(response.content)

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert content == {
        "stock": ["A valid integer is required.",],
    }

@pytest.mark.django_db
def test_create_product_without_category(
    api_client: APIClient, 
    product_url: str,
    product_data: dict, 
):
    
    # Arrange
    new_product: dict = deepcopy(product_data)
    del new_product["category"]

    # Act
    url: str = f"{product_url}/"
    response: WSGIRequest = api_client.post(
        url, 
        data=new_product, 
        format="json",
    )
    content: dict = json.loads(response.content)

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert content == {
        "category": ["This field is required.",],
    }

@pytest.mark.django_db
def test_create_product_with_invalid_category(
    api_client: APIClient, 
    product_url: str,
    product_data: dict, 
):
    
    # Arrange
    new_product: dict = deepcopy(product_data)
    new_product["category"] = ""

    # Act
    url: str = f"{product_url}/"
    response: WSGIRequest = api_client.post(
        url, 
        data=new_product, 
        format="json",
    )
    content: dict = json.loads(response.content)

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert content == {
        "category": ["This field may not be null.",],
    }

@pytest.mark.django_db
def test_get_product(
    api_client: APIClient, 
    product_url: str,
    product: Product,
    product_data: dict, 
):
    
    # Act
    url: str = f"{product_url}/{product.pk}/"
    response: WSGIRequest = api_client.get(url, format="json")
    content: dict = json.loads(response.content)

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert content == product_data

@pytest.mark.django_db
def test_get_not_found_category(
    api_client: APIClient,
    product_url: str,
    id_not_found: int,
    product_not_found: dict,
):
    
    # Act
    url: str = f"{product_url}/{id_not_found}/"
    response: WSGIRequest = api_client.get(url, format="json")
    content: dict = json.loads(response.content)

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert content == product_not_found

@pytest.mark.django_db
def test_update_product(
    api_client: APIClient, 
    product_url: str, 
    product_data: dict, 
):
    
    # Arrange
    product_updated: dict = deepcopy(product_data)
    product_updated["name"] = random_str()

    # Act
    id: int = product_data["id"]
    url: str = f"{product_url}/{id}/"
    response: WSGIRequest = api_client.put(
        url, 
        data=product_updated, 
        format="json",
    )
    content: dict = json.loads(response.content)

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert content == product_updated

@pytest.mark.django_db
def test_update_not_found_product(
    api_client: APIClient, 
    product_url: str,
    id_not_found: int,
    product_data: dict, 
    product_not_found: dict,
):
    
    # Arrange
    product_updated: dict = deepcopy(product_data)
    product_updated["name"] = random_numbers()

    # Act
    url: str = f"{product_url}/{id_not_found}/"
    response: WSGIRequest = api_client.put(
        url, 
        data=product_updated, 
        format="json",
    )
    content: dict = json.loads(response.content)

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert content == product_not_found

@pytest.mark.django_db
def test_delete_product(
    api_client: APIClient, 
    product_url: str,
    product: Product,
    product_deleted_message: dict,
):

    # Act
    url: str = f"{product_url}/{product.pk}/"
    response: WSGIRequest = api_client.delete(url, format="json")

    # Assert
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.data == product_deleted_message

@pytest.mark.django_db
def test_delete_not_found_product(
    api_client: APIClient, 
    product_url: str,
    id_not_found: int,
    product: Product,
    product_not_found: dict,
):

    # Act
    url: str = f"{product_url}/{id_not_found}/"
    response: WSGIRequest = api_client.delete(url, format="json")
    content: dict = json.loads(response.content)

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert content == product_not_found
