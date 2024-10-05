# Market API

## Overview

This project aims to present a [**REST API**](https://aws.amazon.com/pt/what-is/restful-api) for a market system. The entities considered for the market are: customers, employees, categories, products and sales.

## Installation

The project was built using the [**Python**](https://www.python.org/) programming language and the package manager [**PIP**](https://pypi.org/project/pip/). The project's foundation is built with [**Django framework**](https://www.djangoproject.com/), along with the libraries [*django-rest-framework*](https://www.django-rest-framework.org/), [*reportlab*](https://www.reportlab.com/) for PDF generation, and [*pytest*](https://docs.pytest.org/en/stable/) for testing.

To run the project, it is necessary to execute the migrations:

```shell
python manage.py migrate
```

And then, run the server:"

```shell
python manage.py runserver
```

The tests can be executed using the following command:

```shell
pytest --cov
```

A collection using [**Postman API**](https://www.postman.com/) is saved at the root of the project with the name: `market_api.json`.

## Architecture

The project's architecture was built according to the entities. Therefore, the main folder is named `market`, which contains the global settings of the project.

As a Django project, the following apps have been defined:

- Customers
- Employees
- Products
- Sales

Each app follows the standard described by Django: `admin`, `apps`, `models`,  `serializers`, `tests`, `urls`, and `views`.

The `tests` file contains the endpoint tests for each app.

## Models

Each app describes the entity models for the in the `models` file.

**Customer** class:

- document: str (unique)
- name: str
- type: str ("F" or "J")
- email: str
- phone: str
- created_at: date

**Employee** class:

- document: str (unique)
- name: str
- department: str
- hire_date: date
- phone: str
- email: str
- created_at: date

**Category** class:

- name: str
- description: str
- created_at: date

**Product** class:

- name: str
- description: str
- price: float
- stock: int
- created_at: date
- category: Category (Foreign Key)

**Sale** class:

- date: datetime.date
- hour: datetime.time
- status: str ("PAGO", "PENDENTE", "CANCELADO")
- discount: float
- total_amount: float
- payment: str ("DINHEIRO", "CHEQUE", "DEBITO", "CREDITO", "PIX", "VALE_ALIMENTACAO")
- created_at: datetime.datetime
- category: Category (Foreign Key)

**SaleItem** class:

- sale: Sale (Foreign Key)
- product: Product (Foreign Key)
- quantity: int
- unit_price: float
- total_price: float
- discount: float

## Endpoints

Each app describes the endpoints for the corresponding entities in the `urls` file.

### Customers

With the following endpoints:

- GET `/customers/`: return all customers.
- POST `/customers/`: create a new customer.
- GET `/customers/<id>`: get a customer by id.
- PUT `/customers/<id>`: update values from a customer by id.
- DELETE `/customers/<id>`: remove a customer by id.

### Employees

With the following endpoints:

- GET `/employees/`: return all employees.
- POST `/employees/`: create a new employee.
- GET `/employees/<id>`: get a employee by id.
- PUT `/employees/<id>`: update values from a employee by id.
- DELETE `/employees/<id>`: remove a employee by id.

### Products

With the following endpoints:

- GET `/categories/`: return all categories.
- POST `/categories/`: create a new category.
- GET `/categories/<id>`: get a category by id.
- PUT `/categories/<id>`: update values from a category by id.
- DELETE `/categories/<id>`: remove a category by id.
- GET `/products/`: return all products.
- POST `/products/`: create a new product.
- GET `/products/<id>`: get a product by id.
- PUT `/products/<id>`: update values from a product by id.
- DELETE `/products/<id>`: remove a product by id.

### Sales

With the following endpoints:

- GET `/sales/`: return all sales.
- GET `/sales/customer/<id_customer>/?export=<format>`: return sales by a customer, with option to export in csv or pdf format.
- GET `/sales/employee/<id_employee>/?export=<format>`: return sales by an employee, with option to export in csv or pdf format.
- GET `/sales/period/?start_date=<date>&end_date=<date>&export=<format>`: return sales by an period (start date and end date), with option to export in csv or pdf format.
- POST `/sales/`: create a new sale.
- GET `/sales/<id>`: get a sale by id.
- PUT `/sales/<id>`: update values from a sale by id.
- DELETE `/sales/<id>`: remove a sale by id.
