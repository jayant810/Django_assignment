from django.db import models
from core.models import BaseModel
from vendor.models import Vendor
from product.models import Product

class VendorProductMapping(BaseModel):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='product_mappings')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='vendor_mappings')
    primary_mapping = models.BooleanField(default=False)

    class Meta:
        unique_together = ('vendor', 'product')

    def save(self, *args, **kwargs):
        if self.primary_mapping:
            # Set all other mappings for this vendor to False
            VendorProductMapping.objects.filter(vendor=self.vendor, primary_mapping=True).exclude(pk=self.pk).update(primary_mapping=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.vendor.name} -> {self.product.name}"
