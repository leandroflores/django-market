from .models import Customer
from .serializers import CustomerSerializer
from market.views import CRUDAPIView

class CustomerAPIView(CRUDAPIView):
    serializer_class = CustomerSerializer
    
    def model_name(self) -> str:
        return "Customer"

    def get_model(self) -> Customer:
        return Customer
    
    def get_serializer(self) -> CustomerSerializer:
        return CustomerSerializer

    def list_model(self) -> list:
        return Customer.objects.all().order_by("name")
    