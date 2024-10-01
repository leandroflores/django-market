from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from .models import Sale
from .serializers import SaleSerializer
from market.views import CRUDAPIView

class SaleAPIView(CRUDAPIView):
    serializer_class = SaleSerializer
    
    def model_name(self) -> str:
        return "Sale"

    def get_model(self) -> Sale:
        return Sale
    
    def get_serializer(self) -> SaleSerializer:
        return SaleSerializer

    def list_model(self) -> list:
        return Sale.objects.all().order_by("date", "hour")
