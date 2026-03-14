from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Certification
from .serializers import CertificationSerializer
from core.utils import get_object_or_error
from course_certification_mapping.models import CourseCertificationMapping

class CertificationListCreateAPIView(APIView):
    """
    List certifications or create a new certification.
    Supports filtering by course_id.
    """
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('course_id', openapi.IN_QUERY, description="Filter by Course ID", type=openapi.TYPE_INTEGER)
        ],
        responses={200: CertificationSerializer(many=True)},
        operation_description="Get list of certifications"
    )
    def get(self, request):
        course_id = request.query_params.get('course_id')
        queryset = Certification.objects.all()
        
        if course_id:
            cert_ids = CourseCertificationMapping.objects.filter(course_id=course_id, is_active=True).values_list('certification_id', flat=True)
            queryset = queryset.filter(id__in=cert_ids)
            
        serializer = CertificationSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=CertificationSerializer,
        responses={201: CertificationSerializer(), 400: "Bad Request"},
        operation_description="Create a new certification"
    )
    def post(self, request):
        serializer = CertificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CertificationDetailAPIView(APIView):
    """
    Retrieve, update or delete a certification instance.
    """
    @swagger_auto_schema(
        responses={200: CertificationSerializer(), 404: "Not Found"},
        operation_description="Retrieve a certification"
    )
    def get(self, request, pk):
        certification = get_object_or_error(Certification, pk)
        if not certification:
            return Response({"error": "Certification not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = CertificationSerializer(certification)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=CertificationSerializer,
        responses={200: CertificationSerializer(), 400: "Bad Request", 404: "Not Found"},
        operation_description="Update a certification"
    )
    def put(self, request, pk):
        certification = get_object_or_error(Certification, pk)
        if not certification:
            return Response({"error": "Certification not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = CertificationSerializer(certification, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=CertificationSerializer,
        responses={200: CertificationSerializer(), 400: "Bad Request", 404: "Not Found"},
        operation_description="Partial update a certification"
    )
    def patch(self, request, pk):
        certification = get_object_or_error(Certification, pk)
        if not certification:
            return Response({"error": "Certification not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = CertificationSerializer(certification, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={204: "No Content", 404: "Not Found"},
        operation_description="Delete a certification"
    )
    def delete(self, request, pk):
        certification = get_object_or_error(Certification, pk)
        if not certification:
            return Response({"error": "Certification not found"}, status=status.HTTP_404_NOT_FOUND)
        certification.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
