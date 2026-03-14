from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status

def get_object_or_error(model, pk):
    try:
        return model.objects.get(pk=pk)
    except model.DoesNotExist:
        return None
