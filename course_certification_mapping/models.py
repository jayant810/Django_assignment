from django.db import models
from core.models import BaseModel
from course.models import Course
from certification.models import Certification

class CourseCertificationMapping(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='certification_mappings')
    certification = models.ForeignKey(Certification, on_delete=models.CASCADE, related_name='course_mappings')
    primary_mapping = models.BooleanField(default=False)

    class Meta:
        unique_together = ('course', 'certification')

    def save(self, *args, **kwargs):
        if self.primary_mapping:
            # Set all other mappings for this course to False
            CourseCertificationMapping.objects.filter(course=self.course, primary_mapping=True).exclude(pk=self.pk).update(primary_mapping=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.course.name} -> {self.certification.name}"
