from .models import Employee
from .serializers import EmployeeSerializer
from market.views import CRUDAPIView

class EmployeeAPIView(CRUDAPIView):
    serializer_class = EmployeeSerializer
    
    def model_name(self) -> str:
        return "Employee"

    def get_model(self) -> Employee:
        return Employee
    
    def get_serializer(self) -> EmployeeSerializer:
        return EmployeeSerializer

    def list_model(self) -> list:
        return Employee.objects.all().order_by("name")
    
    