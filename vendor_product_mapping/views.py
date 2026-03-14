from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import VendorProductMapping
from .serializers import VendorProductMappingSerializer
from core.utils import get_object_or_error

class VendorProductMappingListCreateAPIView(APIView):
    """
    List vendor-product mappings or create a new one.
    """
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('vendor_id', openapi.IN_QUERY, description="Filter by Vendor ID", type=openapi.TYPE_INTEGER)
        ],
        responses={200: VendorProductMappingSerializer(many=True)},
        operation_description="Get list of vendor-product mappings"
    )
    def get(self, request):
        vendor_id = request.query_params.get('vendor_id')
        queryset = VendorProductMapping.objects.select_related('vendor', 'product').all()
        if vendor_id:
            queryset = queryset.filter(vendor_id=vendor_id)
        serializer = VendorProductMappingSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=VendorProductMappingSerializer,
        responses={201: VendorProductMappingSerializer(), 400: "Bad Request"},
        operation_description="Create a new vendor-product mapping"
    )
    def post(self, request):
        serializer = VendorProductMappingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VendorProductMappingDetailAPIView(APIView):
    """
    Retrieve, update or delete a vendor-product mapping.
    """
    @swagger_auto_schema(
        responses={200: VendorProductMappingSerializer(), 404: "Not Found"},
        operation_description="Retrieve a mapping"
    )
    def get(self, request, pk):
        mapping = get_object_or_error(VendorProductMapping, pk)
        if not mapping:
            return Response({"error": "Mapping not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = VendorProductMappingSerializer(mapping)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=VendorProductMappingSerializer,
        responses={200: VendorProductMappingSerializer(), 400: "Bad Request", 404: "Not Found"},
        operation_description="Update a mapping"
    )
    def put(self, request, pk):
        mapping = get_object_or_error(VendorProductMapping, pk)
        if not mapping:
            return Response({"error": "Mapping not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = VendorProductMappingSerializer(mapping, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=VendorProductMappingSerializer,
        responses={200: VendorProductMappingSerializer(), 400: "Bad Request", 404: "Not Found"},
        operation_description="Partial update a mapping"
    )
    def patch(self, request, pk):
        mapping = get_object_or_error(VendorProductMapping, pk)
        if not mapping:
            return Response({"error": "Mapping not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = VendorProductMappingSerializer(mapping, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={204: "No Content", 404: "Not Found"},
        operation_description="Delete a mapping"
    )
    def delete(self, request, pk):
        mapping = get_object_or_error(VendorProductMapping, pk)
        if not mapping:
            return Response({"error": "Mapping not found"}, status=status.HTTP_404_NOT_FOUND)
        mapping.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
