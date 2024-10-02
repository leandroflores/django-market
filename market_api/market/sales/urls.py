from django.urls import re_path
from .views import SaleAPIView, SalesFilterAPIView

urlpatterns = [
    re_path(
        r"^sales/$", 
        SaleAPIView.as_view(
            {
                "get": "list", 
                "post": "create",
            }
        ),
    ),
    re_path(
        r"^sales/(?P<id>[0-9]+)/$", 
        SaleAPIView.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "delete": "destroy",
            }
        ),
    ),
    re_path(
        r"^sales/customer/(?P<id_customer>\d+)/$", 
        SalesFilterAPIView.as_view(
            {
                "get": "sales_by_customer",
            }
        ),
    ),
    re_path(
        r"^sales/employee/(?P<id_employee>\d+)/$", 
        SalesFilterAPIView.as_view(
            {
                "get": "sales_by_employee",
            }
        ),
    ),
    re_path(
        r"^sales/period/$", 
        SalesFilterAPIView.as_view(
            {
                "get": "sales_by_period",
            }
        ),
    ),
]
