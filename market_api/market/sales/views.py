from datetime import date
from rest_framework import status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Sale
from .serializers import SaleSerializer
from market.utils import to_date
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

class SalesFilterAPIView(viewsets.ModelViewSet):

    def sales_by_customer(self, request: Request, id_customer: int = None) -> Response:
        sales_by_customer = Sale.objects.filter(customer__id=id_customer)
        serializer: SaleSerializer = SaleSerializer(sales_by_customer, many=True)
        return Response(
            {
                "customer_id": id_customer,
                "sales": serializer.data,
            }
        )
    
    def sales_by_employee(self, request: Request, id_employee: int = None) -> Response:
        sales_by_employee = Sale.objects.filter(employee__id=id_employee)
        serializer: SaleSerializer = SaleSerializer(sales_by_employee, many=True)
        return Response(
            {
                "employee_id": id_employee,
                "sales": serializer.data,
            }
        )
    
    def sales_by_period(self, request: Request) -> Response:
        format_date: str = "YYYY-MM-DD"
        start_date: date = to_date(request.query_params.get("start_date"))
        end_date: date = to_date(request.query_params.get("end_date"))
        
        if not start_date or not end_date:
            return Response(
                data=f"'start_date' and 'end_date' are required in format: {format_date}",
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        sales_by_period = Sale.objects.filter(date__range=(start_date, end_date))
        serializer: SaleSerializer = SaleSerializer(sales_by_period, many=True)
        return Response(
            {
                "start_date": start_date.isoformat(),
                "end_date": start_date.isoformat(),
                "sales": serializer.data,
            }
        )
