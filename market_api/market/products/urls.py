from django.urls import re_path
from .views import CategoryAPIView, ProductAPIView

urlpatterns = [
    re_path(
        r"^categories/$", 
        CategoryAPIView.as_view({
            "get": "list", 
            "post": "create",
        }),
    ),
    re_path(
        r"^categories/(?P<id>[0-9]+)/$", 
        CategoryAPIView.as_view({
            "get": "retrieve",
            "put": "update",
            "delete": "destroy",
        }),
    ),
    re_path(
        r"^products/$", 
        ProductAPIView.as_view({
            "get": "list", 
            "post": "create",
        }),
    ),
    re_path(
        r"^products/(?P<id>[0-9]+)/$", 
        ProductAPIView.as_view({
            "get": "retrieve",
            "put": "update",
            "delete": "destroy",
        }),
    ),
]
