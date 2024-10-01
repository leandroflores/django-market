from django.urls import re_path
from .views import EmployeeAPIView

urlpatterns = [
    re_path(
        r"^employees/$", 
        EmployeeAPIView.as_view({
            "get": "list", 
            "post": "create",
        }),
    ),
    re_path(
        r"^employees/(?P<id>[0-9]+)/$", 
        EmployeeAPIView.as_view({
            "get": "retrieve",
            "put": "update",
            "delete": "destroy",
        }),
    ),
]
