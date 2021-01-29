import json
from flask import Response
from flask_jwt_extended import verify_jwt_in_request, get_jwt_claims
from flask_api import status
from .errors import Err, ErrForbidden, ErrUnauthorized


def api_exception_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Err as e:
            return Response(
                status=e.status_code,
                response=json.dumps({'error': e.msg}) if e.msg is not None else None,
                mimetype="application/json"
            )
        except Exception as e:
            return Response(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                response=e.__str__()
            )

    wrapper.__name__ = func.__name__
    return wrapper


def roles_required(roles):
    def wrapper(func):
        def wrapped(*args, **kwargs):
            try:
                verify_jwt_in_request()
            except Exception as e:
                raise ErrUnauthorized()
            claims = get_jwt_claims()
            role = claims["role"]
            if role in roles:
                return func(*args, **kwargs)
            raise ErrForbidden()

        wrapped.__name__ = func.__name__
        return wrapped

    return wrapper
