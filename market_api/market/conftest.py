import pytest

from clients.models import Customer
from clients.serializers import CustomerSerializer
from employees.models import Employee
from employees.serializers import EmployeeSerializer
from market.utils import (
    random_int,
    random_numbers, 
    random_str, 
    today,
    today_datetime,
)
from products.models import Category, Product
from products.serializers import CategorySerializer, ProductSerializer
from sales.models import (
    PAYMENT_CHOICES,
    Sale, 
    SaleItem,
    STATUS_CHOICES,
)
from sales.serializers import SaleSerializer
from rest_framework.test import APIClient

@pytest.fixture
def api_client() -> APIClient:
    return APIClient()

@pytest.fixture
def id_not_found() -> int:
    return random_int(min=500)

@pytest.fixture
def customer_url() -> str:
    return "/customers"

@pytest.fixture
def employee_url() -> str:
    return "/employees"

@pytest.fixture
def category_url() -> str:
    return "/categories"

@pytest.fixture
def product_url() -> str:
    return "/products"

@pytest.fixture
def sale_url() -> str:
    return "/sales"

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
def employee_values() -> dict:
    return {
        "id": 1,
        "document": random_numbers(),
        "name": random_str(),
        "department": "Sales",
        "hire_date": today(),
        "phone": "",
        "email": f"{random_str()}@mail.com",
        "created_at": today(),
    }

@pytest.fixture
def category_values() -> dict:
    return {
        "id": 1,
        "name": random_str(),
        "description": "",
        "created_at": today(),
    }

@pytest.fixture
def product_values() -> dict:
    return {
        "id": 1,
        "name": random_str(),
        "description": "",
        "price": 10.00,
        "stock": 100,
        "created_at": today_datetime(),
    }

@pytest.fixture
def sale_item_values() -> dict:
    return {
        "id": 1,
        "quantity": 2,
        "unit_price": 10.00,
        "total_price": 20.00,
        "discount": 0.00,
    }

@pytest.fixture
def sale_values() -> dict:
    return {
        "id": 1,
        "date": today(),
        "hour": today_datetime().time(),
        "status": STATUS_CHOICES[0][0],
        "discount": 0.00,
        "total_amount": 20.00,
        "payment": PAYMENT_CHOICES[0][0],
        "created_at": today_datetime(),
    }

@pytest.fixture
def customer_not_found() -> dict:
    return {
        "message": "Customer not found",
    }

@pytest.fixture
def employee_not_found() -> dict:
    return {
        "message": "Employee not found",
    }

@pytest.fixture
def category_not_found() -> dict:
    return {
        "message": "Category not found",
    }

@pytest.fixture
def product_not_found() -> dict:
    return {
        "message": "Product not found",
    }

@pytest.fixture
def sale_not_found() -> dict:
    return {
        "message": "Sale not found",
    }

@pytest.fixture
def customer_deleted_message() -> dict:
    return {
        "message": "Customer deleted",
    }

@pytest.fixture
def employee_deleted_message() -> dict:
    return {
        "message": "Employee deleted",
    }

@pytest.fixture
def category_deleted_message() -> dict:
    return {
        "message": "Category deleted",
    }

@pytest.fixture
def product_deleted_message() -> dict:
    return {
        "message": "Product deleted",
    }

@pytest.fixture
def sale_deleted_message() -> dict:
    return {
        "message": "Sale deleted",
    }

@pytest.fixture
def customer_data(customer: Customer) -> dict:
    return CustomerSerializer(customer).data

@pytest.fixture
def employee_data(employee: Employee) -> dict:
    return EmployeeSerializer(employee).data

@pytest.fixture
def category_data(category: Category) -> dict:
    return CategorySerializer(category).data

@pytest.fixture
def product_data(product: Product) -> dict:
    return ProductSerializer(product).data

@pytest.fixture
def sale_data(sale: Sale) -> dict:
    return SaleSerializer(sale).data

@pytest.fixture
def customer(customer_values: dict) -> Customer:
    return Customer.objects.create(**customer_values)

@pytest.fixture
def employee(employee_values: dict) -> Employee:
    return Employee.objects.create(**employee_values)

@pytest.fixture
def category(category_values: dict) -> Category:
    return Category.objects.create(**category_values)

@pytest.fixture
def product(product_values: dict, category: Category) -> Product:
    product: Product = Product(**product_values)
    product.category = category
    product.save()
    return product

@pytest.fixture
def sale(
        sale_values: dict, 
        customer: Customer,
        employee: Employee,
        sale_item_values: dict,
) -> Sale:
    
    sale: Sale = Sale(**sale_values)
    sale.customer = customer
    sale.employee = employee
    sale.save()

    item: SaleItem = SaleItem(**sale_item_values)
    item.sale = sale

    return sale
