import json
from uuid import uuid4
from datetime import datetime
from flask import Response
from flask_api import status
from flask_jwt_extended import get_jwt_claims
from app import jwt


def gen_id() -> str:
    return uuid4().hex


def datetime_now() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat(' ')


def parse_datetime(dt):
    return datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')


def send_ok(msg=None, status_code=status.HTTP_200_OK):
    return Response(status=status_code,
                    response=json.dumps(msg) if msg is not None else None,
                    mimetype="application/json")


def calc_skip(page: int, size: int):
    return (page - 1) * size


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user["_id"]


@jwt.user_claims_loader
def add_claims_to_access_token(user):
    return {"role": user["role"]}


@jwt.user_loader_callback_loader
def user_loader(jwt_identity):
    class CurrUser:
        def __init__(self, identity, is_customer=False, is_staff=False, is_manager=False):
            self.identity = identity
            self.is_customer = is_customer
            self.is_staff = is_staff
            self.is_manager = is_manager

    claims = get_jwt_claims()
    claim_role = claims["role"]
    curr_user = CurrUser(jwt_identity,
                         is_customer=True if "CUSTOMER" == claim_role else False,
                         is_staff=True if "STAFF" == claim_role else False,
                         is_manager=True if "MANAGER" == claim_role else False,
                         )
    return curr_user
