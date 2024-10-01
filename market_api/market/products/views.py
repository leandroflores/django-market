from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from market.views import CRUDAPIView

class CategoryAPIView(CRUDAPIView):
    serializer_class = CategorySerializer
    
    def model_name(self) -> str:
        return "Category"
    
    @property
    def plural_name(self) -> str:
        return "Categories"

    def get_model(self) -> Category:
        return Category
    
    def get_serializer(self) -> CategorySerializer:
        return CategorySerializer

    def list_model(self) -> list:
        return Category.objects.all().order_by("name")

class ProductAPIView(CRUDAPIView):
    serializer_class = ProductSerializer
    
    def model_name(self) -> str:
        return "Product"

    def get_model(self) -> Product:
        return Product
    
    def get_serializer(self) -> ProductSerializer:
        return ProductSerializer

    def list_model(self) -> list:
        return Product.objects.all().order_by("name")
