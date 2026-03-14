from django.db import models
import uuid

class BaseModel(models.Model):
    """
    Abstract base model to provide common fields.
    """
    # Using AutoField/BigAutoField as default for ID if not specified otherwise, 
    # but requirement says 'id', usually it's AutoField.
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
