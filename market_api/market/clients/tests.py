import json

from django.http import HttpResponse
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Customer


class TestCustomerAPIView(APITestCase):

    def setUp(self) -> None:
        self.valid_input: dict = {
            "document": "2313131313",
            "name": "John",
            "type": "F",
        }
        self.customer = Customer.objects.create(**self.valid_input)
        
    
    def test_get_customers(self):
        url: str = "/customers/"
        response: HttpResponse = self.client.get(url, format="json")
        content: dict = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content, {""})
    