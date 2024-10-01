from django.urls import re_path
from .views import SaleAPIView

urlpatterns = [
    re_path(
        r"^sales/$", 
        SaleAPIView.as_view({
            "get": "list", 
            "post": "create",
        }),
    ),
    re_path(
        r"^sales/(?P<id>[0-9]+)/$", 
        SaleAPIView.as_view({
            "get": "retrieve",
            "put": "update",
            "delete": "destroy",
        }),
    ),
]
