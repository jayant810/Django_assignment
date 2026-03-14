from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import ProductCourseMapping
from .serializers import ProductCourseMappingSerializer
from core.utils import get_object_or_error

class ProductCourseMappingListCreateAPIView(APIView):
    """
    List product-course mappings or create a new one.
    """
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('product_id', openapi.IN_QUERY, description="Filter by Product ID", type=openapi.TYPE_INTEGER)
        ],
        responses={200: ProductCourseMappingSerializer(many=True)},
        operation_description="Get list of product-course mappings"
    )
    def get(self, request):
        product_id = request.query_params.get('product_id')
        queryset = ProductCourseMapping.objects.select_related('product', 'course').all()
        if product_id:
            queryset = queryset.filter(product_id=product_id)
        serializer = ProductCourseMappingSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=ProductCourseMappingSerializer,
        responses={201: ProductCourseMappingSerializer(), 400: "Bad Request"},
        operation_description="Create a new product-course mapping"
    )
    def post(self, request):
        serializer = ProductCourseMappingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductCourseMappingDetailAPIView(APIView):
    """
    Retrieve, update or delete a product-course mapping.
    """
    @swagger_auto_schema(
        responses={200: ProductCourseMappingSerializer(), 404: "Not Found"},
        operation_description="Retrieve a mapping"
    )
    def get(self, request, pk):
        mapping = get_object_or_error(ProductCourseMapping, pk)
        if not mapping:
            return Response({"error": "Mapping not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductCourseMappingSerializer(mapping)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=ProductCourseMappingSerializer,
        responses={200: ProductCourseMappingSerializer(), 400: "Bad Request", 404: "Not Found"},
        operation_description="Update a mapping"
    )
    def put(self, request, pk):
        mapping = get_object_or_error(ProductCourseMapping, pk)
        if not mapping:
            return Response({"error": "Mapping not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductCourseMappingSerializer(mapping, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=ProductCourseMappingSerializer,
        responses={200: ProductCourseMappingSerializer(), 400: "Bad Request", 404: "Not Found"},
        operation_description="Partial update a mapping"
    )
    def patch(self, request, pk):
        mapping = get_object_or_error(ProductCourseMapping, pk)
        if not mapping:
            return Response({"error": "Mapping not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductCourseMappingSerializer(mapping, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={204: "No Content", 404: "Not Found"},
        operation_description="Delete a mapping"
    )
    def delete(self, request, pk):
        mapping = get_object_or_error(ProductCourseMapping, pk)
        if not mapping:
            return Response({"error": "Mapping not found"}, status=status.HTTP_404_NOT_FOUND)
        mapping.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
