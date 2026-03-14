from rest_framework import serializers
from .models import CourseCertificationMapping

class CourseCertificationMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCertificationMapping
        fields = '__all__'

    def validate(self, data):
        course = data.get('course')
        certification = data.get('certification')
        primary_mapping = data.get('primary_mapping', False)

        if primary_mapping:
            queryset = CourseCertificationMapping.objects.filter(course=course, primary_mapping=True, is_active=True)
            if self.instance:
                queryset = queryset.exclude(pk=self.instance.pk)
            if queryset.exists():
                raise serializers.ValidationError({
                    "primary_mapping": "This course already has a primary certification mapping."
                })

        return data
