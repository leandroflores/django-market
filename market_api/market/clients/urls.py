from django.urls import re_path
from .views import CustomerAPIView

urlpatterns = [
    re_path(
        r"^customers/$", 
        CustomerAPIView.as_view({
            "get": "list", 
            "post": "create",
        }),
    ),
    re_path(
        r"^customers/(?P<id>[0-9]+)/$", 
        CustomerAPIView.as_view({
            "get": "retrieve",
            "put": "update",
            "delete": "destroy",
        }),
    ),
]
