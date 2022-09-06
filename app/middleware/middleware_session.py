from ..models import *
from rest_framework.response import Response
from rest_framework import status
import jwt


def session_middleware(get_response):

    def middleware(request):
        try:
            token = request.META.get('HTTP_AUTHORIZATION').split()

            user = jwt.decode(token[1], key='my_super_secret',
                              algorithms=['HS256', ])

            request.curr_user = user
            response = get_response(request)
            return response

        except Exception as e:
            request.error = str(e)
            response = get_response(request)
            return response

    return middleware
