from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import CourseCertificationMapping
from .serializers import CourseCertificationMappingSerializer
from core.utils import get_object_or_error

class CourseCertificationMappingListCreateAPIView(APIView):
    """
    List course-certification mappings or create a new one.
    """
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('course_id', openapi.IN_QUERY, description="Filter by Course ID", type=openapi.TYPE_INTEGER)
        ],
        responses={200: CourseCertificationMappingSerializer(many=True)},
        operation_description="Get list of course-certification mappings"
    )
    def get(self, request):
        course_id = request.query_params.get('course_id')
        queryset = CourseCertificationMapping.objects.select_related('course', 'certification').all()
        if course_id:
            queryset = queryset.filter(course_id=course_id)
        serializer = CourseCertificationMappingSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=CourseCertificationMappingSerializer,
        responses={201: CourseCertificationMappingSerializer(), 400: "Bad Request"},
        operation_description="Create a new course-certification mapping"
    )
    def post(self, request):
        serializer = CourseCertificationMappingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CourseCertificationMappingDetailAPIView(APIView):
    """
    Retrieve, update or delete a course-certification mapping.
    """
    @swagger_auto_schema(
        responses={200: CourseCertificationMappingSerializer(), 404: "Not Found"},
        operation_description="Retrieve a mapping"
    )
    def get(self, request, pk):
        mapping = get_object_or_error(CourseCertificationMapping, pk)
        if not mapping:
            return Response({"error": "Mapping not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = CourseCertificationMappingSerializer(mapping)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=CourseCertificationMappingSerializer,
        responses={200: CourseCertificationMappingSerializer(), 400: "Bad Request", 404: "Not Found"},
        operation_description="Update a mapping"
    )
    def put(self, request, pk):
        mapping = get_object_or_error(CourseCertificationMapping, pk)
        if not mapping:
            return Response({"error": "Mapping not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = CourseCertificationMappingSerializer(mapping, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=CourseCertificationMappingSerializer,
        responses={200: CourseCertificationMappingSerializer(), 400: "Bad Request", 404: "Not Found"},
        operation_description="Partial update a mapping"
    )
    def patch(self, request, pk):
        mapping = get_object_or_error(CourseCertificationMapping, pk)
        if not mapping:
            return Response({"error": "Mapping not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = CourseCertificationMappingSerializer(mapping, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={204: "No Content", 404: "Not Found"},
        operation_description="Delete a mapping"
    )
    def delete(self, request, pk):
        mapping = get_object_or_error(CourseCertificationMapping, pk)
        if not mapping:
            return Response({"error": "Mapping not found"}, status=status.HTTP_404_NOT_FOUND)
        mapping.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
