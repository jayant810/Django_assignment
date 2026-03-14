from rest_framework import serializers
from .models import ProductCourseMapping

class ProductCourseMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCourseMapping
        fields = '__all__'

    def validate(self, data):
        product = data.get('product')
        course = data.get('course')
        primary_mapping = data.get('primary_mapping', False)

        if primary_mapping:
            queryset = ProductCourseMapping.objects.filter(product=product, primary_mapping=True, is_active=True)
            if self.instance:
                queryset = queryset.exclude(pk=self.instance.pk)
            if queryset.exists():
                raise serializers.ValidationError({
                    "primary_mapping": "This product already has a primary course mapping."
                })

        return data
