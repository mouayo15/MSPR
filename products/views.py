from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer
from .service_product import publish_products

publish_products()
class ProductListCreate(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        # This method is called when a product is successfully created
        serializer.save()  # Save the new product
        publish_products()  # Publish the updated list of products to RabbitMQ


class ProductRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_update(self, serializer):
        # This method is called when a product is successfully updated
        serializer.save()  # Save the updated product
        publish_products()  # Publish the updated list of products to RabbitMQ

    def perform_destroy(self, instance):
        # This method is called when a product is successfully deleted
        instance.delete()  # Delete the product
        publish_products()  # Publish the updated list of products to RabbitMQ
