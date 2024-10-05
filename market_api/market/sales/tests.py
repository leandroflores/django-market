import json
import pytest

from copy import deepcopy
from datetime import date
from django.core.handlers.wsgi import WSGIRequest
from rest_framework import status
from rest_framework.test import APIClient

from .models import Sale
from market.utils import random_numbers, random_str, today_datetime

@pytest.mark.django_db
def test_get_sales(
    api_client: APIClient, 
    sale_url: str,
    sale: Sale, 
    sale_data: dict,
):
    
    # Act
    url: str = f"{sale_url}/"
    response: WSGIRequest = api_client.get(url, format="json")
    content: dict = json.loads(response.content)

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert content == {
        "Sales": [sale_data]
    }

@pytest.mark.django_db
def test_create_sale(
    api_client: APIClient, 
    sale_url: str,
    sale_data: dict, 
):
    
    # Arrange
    new_sale: dict = deepcopy(sale_data)
    new_sale["id"] = 2
    new_sale["hour"] = str(today_datetime().time())

    # Act
    url: str = f"{sale_url}/"
    response: WSGIRequest = api_client.post(
        url, 
        data=new_sale, 
        format="json",
    )
    content: dict = json.loads(response.content)

    # Assert
    assert response.status_code == status.HTTP_201_CREATED
    assert content["id"] == new_sale["id"]
    assert content["date"] == new_sale["date"]
    assert content["hour"] == new_sale["hour"]
    assert content["status"] == new_sale["status"]
    assert content["discount"] == new_sale["discount"]
    assert content["total_amount"] == new_sale["total_amount"]
    assert content["payment"] == new_sale["payment"]
    assert content["customer"] == new_sale["customer"]
    assert content["employee"] == new_sale["employee"]

@pytest.mark.django_db
def test_create_sale_with_empty_data(
    api_client: APIClient,
    sale_url: str,
):
    
    # Arrange
    new_sale: dict = {}

    # Act
    url: str = f"{sale_url}/"
    response: WSGIRequest = api_client.post(
        url, 
        data=new_sale, 
        format="json",
    )
    content: dict = json.loads(response.content)

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert content == {
        "date": ["This field is required.",],
        "hour": ["This field is required.",],
        "status": ["This field is required.",],
        "total_amount": ["This field is required.",],
        "customer": ["This field is required.",],
        "employee": ["This field is required.",],
        "items": ["This field is required.",],
    }

@pytest.mark.django_db
def test_create_sale_without_date(
    api_client: APIClient, 
    sale_url: str,
    sale_data: dict, 
):
    
    # Arrange
    new_sale: dict = deepcopy(sale_data)
    del new_sale["date"]

    # Act
    url: str = f"{sale_url}/"
    response: WSGIRequest = api_client.post(
        url, 
        data=new_sale, 
        format="json",
    )
    content: dict = json.loads(response.content)

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert content == {
        "date": ["This field is required.",],
    }

@pytest.mark.django_db
def test_create_sale_with_invalid_date(
    api_client: APIClient, 
    sale_url: str,
    sale_data: dict, 
):
    
    # Arrange
    new_sale: dict = deepcopy(sale_data)
    new_sale["date"] = ""

    # Act
    url: str = f"{sale_url}/"
    response: WSGIRequest = api_client.post(
        url, 
        data=new_sale, 
        format="json",
    )
    content: dict = json.loads(response.content)

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert content == {
        "date": ["Date has wrong format. Use one of these formats instead: YYYY-MM-DD.",],
    }

@pytest.mark.django_db
def test_create_sale_without_hour(
    api_client: APIClient, 
    sale_url: str,
    sale_data: dict, 
):
    
    # Arrange
    new_sale: dict = deepcopy(sale_data)
    del new_sale["hour"]

    # Act
    url: str = f"{sale_url}/"
    response: WSGIRequest = api_client.post(
        url, 
        data=new_sale, 
        format="json",
    )
    content: dict = json.loads(response.content)

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert content == {
        "hour": ["This field is required.",],
    }

@pytest.mark.django_db
def test_create_customer_with_invalid_hour(
    api_client: APIClient, 
    sale_url: str,
    sale_data: dict, 
):
    
    # Arrange
    new_sale: dict = deepcopy(sale_data)
    new_sale["hour"] = ""

    # Act
    url: str = f"{sale_url}/"
    response: WSGIRequest = api_client.post(
        url, 
        data=new_sale, 
        format="json",
    )
    content: dict = json.loads(response.content)

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert content == {
        "hour": ["Time has wrong format. Use one of these formats instead: hh:mm[:ss[.uuuuuu]].",],
    }

@pytest.mark.django_db
def test_create_sale_without_status(
    api_client: APIClient, 
    sale_url: str,
    sale_data: dict, 
):
    
    # Arrange
    new_sale: dict = deepcopy(sale_data)
    del new_sale["status"]

    # Act
    url: str = f"{sale_url}/"
    response: WSGIRequest = api_client.post(
        url, 
        data=new_sale, 
        format="json",
    )
    content: dict = json.loads(response.content)

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert content == {
        "status": ["This field is required.",],
    }

@pytest.mark.django_db
def test_create_customer_with_invalid_status(
    api_client: APIClient, 
    sale_url: str,
    sale_data: dict, 
):
    
    # Arrange
    new_sale: dict = deepcopy(sale_data)
    new_sale["status"] = ""

    # Act
    url: str = f"{sale_url}/"
    response: WSGIRequest = api_client.post(
        url, 
        data=new_sale, 
        format="json",
    )
    content: dict = json.loads(response.content)

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert content == {
        "status": ["\"\" is not a valid choice.",],
    }

@pytest.mark.django_db
def test_create_sale_without_total_amount(
    api_client: APIClient, 
    sale_url: str,
    sale_data: dict, 
):
    
    # Arrange
    new_sale: dict = deepcopy(sale_data)
    del new_sale["total_amount"]

    # Act
    url: str = f"{sale_url}/"
    response: WSGIRequest = api_client.post(
        url, 
        data=new_sale, 
        format="json",
    )
    content: dict = json.loads(response.content)

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert content == {
        "total_amount": ["This field is required.",],
    }

@pytest.mark.django_db
def test_create_customer_with_invalid_total_amount(
    api_client: APIClient, 
    sale_url: str,
    sale_data: dict, 
):
    
    # Arrange
    new_sale: dict = deepcopy(sale_data)
    new_sale["total_amount"] = ""

    # Act
    url: str = f"{sale_url}/"
    response: WSGIRequest = api_client.post(
        url, 
        data=new_sale, 
        format="json",
    )
    content: dict = json.loads(response.content)

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert content == {
        "total_amount": ["A valid number is required.",],
    }


@pytest.mark.django_db
def test_create_sale_without_customer(
    api_client: APIClient, 
    sale_url: str,
    sale_data: dict, 
):
    
    # Arrange
    new_sale: dict = deepcopy(sale_data)
    del new_sale["customer"]

    # Act
    url: str = f"{sale_url}/"
    response: WSGIRequest = api_client.post(
        url, 
        data=new_sale, 
        format="json",
    )
    content: dict = json.loads(response.content)

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert content == {
        "customer": ["This field is required.",],
    }

@pytest.mark.django_db
def test_create_sale_with_invalid_customer(
    api_client: APIClient, 
    sale_url: str,
    sale_data: dict, 
):
    
    # Arrange
    new_sale: dict = deepcopy(sale_data)
    new_sale["customer"] = ""

    # Act
    url: str = f"{sale_url}/"
    response: WSGIRequest = api_client.post(
        url, 
        data=new_sale, 
        format="json",
    )
    content: dict = json.loads(response.content)

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert content == {
        "customer": ["This field may not be null.",],
    }

@pytest.mark.django_db
def test_create_sale_without_employee(
    api_client: APIClient, 
    sale_url: str,
    sale_data: dict, 
):
    
    # Arrange
    new_sale: dict = deepcopy(sale_data)
    del new_sale["employee"]

    # Act
    url: str = f"{sale_url}/"
    response: WSGIRequest = api_client.post(
        url, 
        data=new_sale, 
        format="json",
    )
    content: dict = json.loads(response.content)

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert content == {
        "employee": ["This field is required.",],
    }

@pytest.mark.django_db
def test_create_sale_with_invalid_employee(
    api_client: APIClient, 
    sale_url: str,
    sale_data: dict, 
):
    
    # Arrange
    new_sale: dict = deepcopy(sale_data)
    new_sale["employee"] = ""

    # Act
    url: str = f"{sale_url}/"
    response: WSGIRequest = api_client.post(
        url, 
        data=new_sale, 
        format="json",
    )
    content: dict = json.loads(response.content)

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert content == {
        "employee": ["This field may not be null.",],
    }

@pytest.mark.django_db
def test_create_sale_without_items(
    api_client: APIClient, 
    sale_url: str,
    sale_data: dict, 
):
    
    # Arrange
    new_sale: dict = deepcopy(sale_data)
    del new_sale["items"]

    # Act
    url: str = f"{sale_url}/"
    response: WSGIRequest = api_client.post(
        url, 
        data=new_sale, 
        format="json",
    )
    content: dict = json.loads(response.content)

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert content == {
        "items": ["This field is required.",],
    }

@pytest.mark.django_db
def test_create_sale_with_invalid_items(
    api_client: APIClient, 
    sale_url: str,
    sale_data: dict, 
):
    
    # Arrange
    new_sale: dict = deepcopy(sale_data)
    new_sale["items"] = None

    # Act
    url: str = f"{sale_url}/"
    response: WSGIRequest = api_client.post(
        url, 
        data=new_sale, 
        format="json",
    )
    content: dict = json.loads(response.content)

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert content == {
        "items": ["This field may not be null.",],
    }

@pytest.mark.django_db
def test_get_sale(
    api_client: APIClient, 
    sale_url: str,
    sale: Sale,
    sale_data: dict, 
):
    
    # Act
    url: str = f"{sale_url}/{sale.pk}/"
    response: WSGIRequest = api_client.get(url, format="json")
    content: dict = json.loads(response.content)

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert content == sale_data

@pytest.mark.django_db
def test_get_not_found_sale(
    api_client: APIClient,
    sale_url: str,
    id_not_found: int,
    sale_not_found: dict,
):
    
    # Act
    url: str = f"{sale_url}/{id_not_found}/"
    response: WSGIRequest = api_client.get(url, format="json")
    content: dict = json.loads(response.content)

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert content == sale_not_found

@pytest.mark.django_db
def test_update_sale(
    api_client: APIClient, 
    sale_url: str, 
    sale_data: dict, 
):
    
    # Arrange
    sale_updated: dict = deepcopy(sale_data)
    sale_updated["hour"] = str(today_datetime().time())

    # Act
    id: int = sale_data["id"]
    url: str = f"{sale_url}/{id}/"
    response: WSGIRequest = api_client.put(
        url, 
        data=sale_updated, 
        format="json",
    )
    content: dict = json.loads(response.content)

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert content == sale_updated

@pytest.mark.django_db
def test_update_not_found_sale(
    api_client: APIClient, 
    sale_url: str,
    id_not_found: int,
    sale_data: dict, 
    sale_not_found: dict,
):
    
    # Arrange
    sale_updated: dict = deepcopy(sale_data)
    sale_updated["hour"] = str(today_datetime().time())

    # Act
    url: str = f"{sale_url}/{id_not_found}/"
    response: WSGIRequest = api_client.put(
        url, 
        data=sale_updated, 
        format="json",
    )
    content: dict = json.loads(response.content)

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert content == sale_not_found

@pytest.mark.django_db
def test_delete_sale(
    api_client: APIClient, 
    sale_url: str,
    sale: Sale,
    sale_deleted_message: dict,
):

    # Act
    url: str = f"{sale_url}/{sale.pk}/"
    response: WSGIRequest = api_client.delete(url, format="json")

    # Assert
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.data == sale_deleted_message

@pytest.mark.django_db
def test_delete_not_found_sale(
    api_client: APIClient, 
    sale_url: str,
    id_not_found: int,
    sale_not_found: dict,
):

    # Act
    url: str = f"{sale_url}/{id_not_found}/"
    response: WSGIRequest = api_client.delete(url, format="json")
    content: dict = json.loads(response.content)

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert content == sale_not_found


@pytest.mark.django_db
def test_get_sales_by_customer(
    api_client: APIClient, 
    sale_url: str,
    customer_data: dict,
    sale_data: dict,
):
    
    # Arrange
    id_customer: int = customer_data["id"]
    
    # Act
    url: str = f"{sale_url}/customer/{id_customer}/"
    response: WSGIRequest = api_client.get(url, format="json")
    content: dict = json.loads(response.content)

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert content == {
        "customer_id": f"{id_customer}",
        "sales": [sale_data]
    }

@pytest.mark.django_db
def test_get_sales_by_customer_not_found(
    api_client: APIClient, 
    sale_url: str,
    id_not_found: int,
    sale_data: dict,
):
    
    # Arrange
    id_customer: int = id_not_found
    
    # Act
    url: str = f"{sale_url}/customer/{id_customer}/"
    response: WSGIRequest = api_client.get(url, format="json")
    content: dict = json.loads(response.content)

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert content == {
        "customer_id": f"{id_customer}",
        "sales": []
    }

@pytest.mark.django_db
def test_get_sales_by_employee(
    api_client: APIClient, 
    sale_url: str,
    employee_data: dict,
    sale_data: dict,
):
    
    # Arrange
    id_employee: int = employee_data["id"]
    
    # Act
    url: str = f"{sale_url}/employee/{id_employee}/"
    response: WSGIRequest = api_client.get(url, format="json")
    content: dict = json.loads(response.content)

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert content == {
        "employee_id": f"{id_employee}",
        "sales": [sale_data]
    }

@pytest.mark.django_db
def test_get_sales_by_employee_not_found(
    api_client: APIClient, 
    sale_url: str,
    id_not_found: int,
):
    
    # Arrange
    id_employee: int = id_not_found
    
    # Act
    url: str = f"{sale_url}/employee/{id_employee}/"
    response: WSGIRequest = api_client.get(url, format="json")
    content: dict = json.loads(response.content)

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert content == {
        "employee_id": f"{id_employee}",
        "sales": []
    }


@pytest.mark.django_db
def test_get_sales_by_period(
    api_client: APIClient, 
    sale_url: str,
    sale_values: dict,
    sale_data: dict,
):
    
    # Arrange
    sale_date: date = sale_values["date"]
    day: str = sale_date.strftime("%Y-%m-%d")
    
    # Act
    url: str = f"{sale_url}/period/?start_date={day}&end_date={day}"
    response: WSGIRequest = api_client.get(url, format="json")
    content: dict = json.loads(response.content)

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert content == {
        "start_date": f"{day}",
        "end_date": f"{day}",
        "sales": [sale_data]
    }

@pytest.mark.django_db
def test_get_sales_by_period_without_start_date(
    api_client: APIClient, 
    sale_url: str,
    sale_values: dict,
):
    
    # Arrange
    sale_date: date = sale_values["date"]
    day: str = sale_date.strftime("%Y-%m-%d")
    
    # Act
    url: str = f"{sale_url}/period/?end_date={day}"
    response: WSGIRequest = api_client.get(url, format="json")
    content: dict = json.loads(response.content)

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert content == "'start_date' and 'end_date' are required in format: YYYY-MM-DD"

@pytest.mark.django_db
def test_get_sales_by_period_without_end_date(
    api_client: APIClient, 
    sale_url: str,
    sale_values: dict,
):
    
    # Arrange
    sale_date: date = sale_values["date"]
    day: str = sale_date.strftime("%Y-%m-%d")
    
    # Act
    url: str = f"{sale_url}/period/?start_date={day}"
    response: WSGIRequest = api_client.get(url, format="json")
    content: dict = json.loads(response.content)

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert content == "'start_date' and 'end_date' are required in format: YYYY-MM-DD"

