import csv

from datetime import date
from django.db.models import Manager
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
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

    def sales_in_csv(self, sales: Manager[Sale]) -> HttpResponse:
        response: HttpResponse = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename='sales.csv'"

        writer = csv.writer(response)
        writer.writerow(Sale.columns_header())

        for sale in sales:
            writer.writerow(sale.row)

        return response
    
    def sales_in_pdf(self, sales: Manager[Sale]):
        response: HttpResponse = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = "attachment; filename='sales.pdf'"

        pdf: SimpleDocTemplate = SimpleDocTemplate(response, pagesize=A4)
        data = [Sale.columns_header()]
        for sale in sales:
            data.append(sale.row)

        table: Table = Table(data)
        table.setStyle(TableStyle([
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 14),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ]))
        pdf.build([table])

        return response
        

    def sales_by_customer(self, request: Request, id_customer: int = None) -> Response:
        sales_by_customer = Sale.objects.filter(customer__id=id_customer)
        export: str = request.query_params.get("export")

        if export == "csv":
            return self.sales_in_csv(sales_by_customer)
        
        if export == "pdf":
            return self.sales_in_pdf(sales_by_customer)
        
        serializer: SaleSerializer = SaleSerializer(sales_by_customer, many=True)
        return Response(
            {
                "customer_id": id_customer,
                "sales": serializer.data,
            }
        )
    
    def sales_by_employee(self, request: Request, id_employee: int = None) -> Response:
        sales_by_employee = Sale.objects.filter(employee__id=id_employee)
        export: str = request.query_params.get("export")

        if export == "csv":
            return self.sales_in_csv(sales_by_employee)
        
        if export == "pdf":
            return self.sales_in_pdf(sales_by_employee)

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
        export: str = request.query_params.get("export")

        if not start_date or not end_date:
            return Response(
                data=f"'start_date' and 'end_date' are required in format: {format_date}",
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        sales_by_period = Sale.objects.filter(date__range=(start_date, end_date))
        
        if export == "csv":
            return self.sales_in_csv(sales_by_period)
        
        if export == "pdf":
            return self.sales_in_pdf(sales_by_period)

        serializer: SaleSerializer = SaleSerializer(sales_by_period, many=True)
        return Response(
            {
                "start_date": start_date.isoformat(),
                "end_date": start_date.isoformat(),
                "sales": serializer.data,
            }
        )
