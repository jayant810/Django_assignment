from rest_framework import serializers
from .models import VendorProductMapping

class VendorProductMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorProductMapping
        fields = '__all__'

    def validate(self, data):
        # 1. Duplicate mapping prevention (Handled by unique_together but explicit here)
        vendor = data.get('vendor')
        product = data.get('product')
        primary_mapping = data.get('primary_mapping', False)

        # Skip duplicate check if it's an update and same instance (though model clean handles this)
        # But for APIView we often do manual checks or just rely on IntegrityError.
        # Here we'll do a check for primary_mapping constraint.

        if primary_mapping:
            # Check if another primary mapping exists for this vendor
            queryset = VendorProductMapping.objects.filter(vendor=vendor, primary_mapping=True, is_active=True)
            
            # If it's an update, exclude current instance
            if self.instance:
                queryset = queryset.exclude(pk=self.instance.pk)
                
            if queryset.exists():
                raise serializers.ValidationError({
                    "primary_mapping": "This vendor already has a primary product mapping."
                })

        return data
