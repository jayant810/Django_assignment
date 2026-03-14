from django.urls import path
from .views import CourseCertificationMappingListCreateAPIView, CourseCertificationMappingDetailAPIView

urlpatterns = [
    path('course-certification-mappings/', CourseCertificationMappingListCreateAPIView.as_view(), name='course-certification-mapping-list-create'),
    path('course-certification-mappings/<int:pk>/', CourseCertificationMappingDetailAPIView.as_view(), name='course-certification-mapping-detail'),
]
