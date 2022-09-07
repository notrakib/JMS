import json
from django.http import HttpResponseForbidden
from ..models import *
import jwt


def session_middleware(get_response):

    def middleware(request):

        request.curr_user = {
            "id": None,
            "email": None,
            "type": None
        }
        response = get_response(request)
        return response

    return middleware
