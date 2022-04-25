from rest_framework import viewsets
from shop.models import Product
from shop.serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint for product.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()
        category = self.request.GET.get('category')
        if category is not None:
            queryset = queryset.filter(category__id=category)
        return queryset

