import pytest


from clients.models import Customer
from clients.serializers import CustomerSerializer

from market.utils import random_numbers, random_str, today
from rest_framework.test import APIClient

@pytest.fixture
def api_client() -> APIClient:
    return APIClient()

@pytest.fixture
def customer_values() -> dict:
    return {
        "id": 1,
        "document": random_numbers(),
        "name": random_str(),
        "type": "F",
        "email": f"{random_str()}@mail.com",
        "phone": "",
        "created_at": today(),
    }

@pytest.fixture
def customer_not_found() -> dict:
    return {
        "message": "Customer not found",
    }

@pytest.fixture
def customer_deleted_message() -> dict:
    return {
        "message": "Customer deleted",
    }

@pytest.fixture
def customer_data(customer: Customer) -> dict:
    return CustomerSerializer(customer).data

@pytest.fixture
def customer(customer_values: dict) -> Customer:
    return Customer.objects.create(**customer_values)

