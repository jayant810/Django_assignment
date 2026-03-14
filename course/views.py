from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Course
from .serializers import CourseSerializer
from core.utils import get_object_or_error
from product_course_mapping.models import ProductCourseMapping

class CourseListCreateAPIView(APIView):
    """
    List courses or create a new course.
    Supports filtering by product_id.
    """
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('product_id', openapi.IN_QUERY, description="Filter by Product ID", type=openapi.TYPE_INTEGER)
        ],
        responses={200: CourseSerializer(many=True)},
        operation_description="Get list of courses"
    )
    def get(self, request):
        product_id = request.query_params.get('product_id')
        queryset = Course.objects.all()
        
        if product_id:
            course_ids = ProductCourseMapping.objects.filter(product_id=product_id, is_active=True).values_list('course_id', flat=True)
            queryset = queryset.filter(id__in=course_ids)
            
        serializer = CourseSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=CourseSerializer,
        responses={201: CourseSerializer(), 400: "Bad Request"},
        operation_description="Create a new course"
    )
    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CourseDetailAPIView(APIView):
    """
    Retrieve, update or delete a course instance.
    """
    @swagger_auto_schema(
        responses={200: CourseSerializer(), 404: "Not Found"},
        operation_description="Retrieve a course"
    )
    def get(self, request, pk):
        course = get_object_or_error(Course, pk)
        if not course:
            return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = CourseSerializer(course)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=CourseSerializer,
        responses={200: CourseSerializer(), 400: "Bad Request", 404: "Not Found"},
        operation_description="Update a course"
    )
    def put(self, request, pk):
        course = get_object_or_error(Course, pk)
        if not course:
            return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = CourseSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=CourseSerializer,
        responses={200: CourseSerializer(), 400: "Bad Request", 404: "Not Found"},
        operation_description="Partial update a course"
    )
    def patch(self, request, pk):
        course = get_object_or_error(Course, pk)
        if not course:
            return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = CourseSerializer(course, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={204: "No Content", 404: "Not Found"},
        operation_description="Delete a course"
    )
    def delete(self, request, pk):
        course = get_object_or_error(Course, pk)
        if not course:
            return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
