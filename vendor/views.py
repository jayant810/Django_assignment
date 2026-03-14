from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Vendor
from .serializers import VendorSerializer
from core.utils import get_object_or_error

class VendorListCreateAPIView(APIView):
    """
    List vendors or create a new vendor.
    """
    @swagger_auto_schema(
        responses={200: VendorSerializer(many=True)},
        operation_description="Get list of vendors"
    )
    def get(self, request):
        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=VendorSerializer,
        responses={201: VendorSerializer(), 400: "Bad Request"},
        operation_description="Create a new vendor"
    )
    def post(self, request):
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VendorDetailAPIView(APIView):
    """
    Retrieve, update or delete a vendor instance.
    """
    @swagger_auto_schema(
        responses={200: VendorSerializer(), 404: "Not Found"},
        operation_description="Retrieve a vendor"
    )
    def get(self, request, pk):
        vendor = get_object_or_error(Vendor, pk)
        if not vendor:
            return Response({"error": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = VendorSerializer(vendor)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=VendorSerializer,
        responses={200: VendorSerializer(), 400: "Bad Request", 404: "Not Found"},
        operation_description="Update a vendor"
    )
    def put(self, request, pk):
        vendor = get_object_or_error(Vendor, pk)
        if not vendor:
            return Response({"error": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = VendorSerializer(vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=VendorSerializer,
        responses={200: VendorSerializer(), 400: "Bad Request", 404: "Not Found"},
        operation_description="Partial update a vendor"
    )
    def patch(self, request, pk):
        vendor = get_object_or_error(Vendor, pk)
        if not vendor:
            return Response({"error": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = VendorSerializer(vendor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={204: "No Content", 404: "Not Found"},
        operation_description="Delete a vendor"
    )
    def delete(self, request, pk):
        vendor = get_object_or_error(Vendor, pk)
        if not vendor:
            return Response({"error": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)
        vendor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
