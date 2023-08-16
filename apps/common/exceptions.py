from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler
from django.db.utils import IntegrityError
from rest_framework.response import Response
from rest_framework import status


class BadRequest(APIException):
    status_code = 400
    default_detail = "Bad Request"
    default_code = "bad_request"


def custom_exception_handler(exc, context):
    if isinstance(exc, IntegrityError):
        print(type(exc))
        print(exc)
        args = getattr(exc, "args", "args")[0]
        kwargs = args.split("\n", 2)
        data = {
            "status": "error",
            "message": kwargs[0],
            "error": kwargs[1].split("DETAIL:  ")[1],
        }
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    response = exception_handler(exc, context)
    default_data = response.data
    message = default_data.get("detail")
    error = (
        default_data.get("error") or default_data
        if not default_data.get("detail")
        else ""
    )
    data = {"status": "error", "message": message, "error": error}
    response.data = data
    return response
