from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    # Call DRF's default exception handler first to get the standard error response.
    response = exception_handler(exc, context)

    if response is not None:
        custom_res = {
            "status": "error",
            "message": response.data.get("detail", "An error occurred"),
            "errors": response.data,
            "code": response.status_code
        }
        response.data = custom_res
    else:
        # For non-DRF exceptions (like database errors)
        return Response({
            "status": "error",
            "message": str(exc),
            "code": 500
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return response
