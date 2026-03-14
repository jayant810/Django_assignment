from django.db import models
from core.models import BaseModel
from product.models import Product
from course.models import Course

class ProductCourseMapping(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='course_mappings')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='product_mappings')
    primary_mapping = models.BooleanField(default=False)

    class Meta:
        unique_together = ('product', 'course')

    def save(self, *args, **kwargs):
        if self.primary_mapping:
            # Set all other mappings for this product to False
            ProductCourseMapping.objects.filter(product=self.product, primary_mapping=True).exclude(pk=self.pk).update(primary_mapping=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} -> {self.course.name}"
