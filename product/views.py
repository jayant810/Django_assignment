from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Product
from .serializers import ProductSerializer
from core.utils import get_object_or_error
from vendor_product_mapping.models import VendorProductMapping

class ProductListCreateAPIView(APIView):
    """
    List products or create a new product.
    Supports filtering by vendor_id.
    """
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('vendor_id', openapi.IN_QUERY, description="Filter by Vendor ID", type=openapi.TYPE_INTEGER)
        ],
        responses={200: ProductSerializer(many=True)},
        operation_description="Get list of products"
    )
    def get(self, request):
        vendor_id = request.query_params.get('vendor_id')
        queryset = Product.objects.all()
        
        if vendor_id:
            # Filter products mapped to this vendor
            product_ids = VendorProductMapping.objects.filter(vendor_id=vendor_id, is_active=True).values_list('product_id', flat=True)
            queryset = queryset.filter(id__in=product_ids)
            
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=ProductSerializer,
        responses={201: ProductSerializer(), 400: "Bad Request"},
        operation_description="Create a new product"
    )
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDetailAPIView(APIView):
    """
    Retrieve, update or delete a product instance.
    """
    @swagger_auto_schema(
        responses={200: ProductSerializer(), 404: "Not Found"},
        operation_description="Retrieve a product"
    )
    def get(self, request, pk):
        product = get_object_or_error(Product, pk)
        if not product:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=ProductSerializer,
        responses={200: ProductSerializer(), 400: "Bad Request", 404: "Not Found"},
        operation_description="Update a product"
    )
    def put(self, request, pk):
        product = get_object_or_error(Product, pk)
        if not product:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=ProductSerializer,
        responses={200: ProductSerializer(), 400: "Bad Request", 404: "Not Found"},
        operation_description="Partial update a product"
    )
    def patch(self, request, pk):
        product = get_object_or_error(Product, pk)
        if not product:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={204: "No Content", 404: "Not Found"},
        operation_description="Delete a product"
    )
    def delete(self, request, pk):
        product = get_object_or_error(Product, pk)
        if not product:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
