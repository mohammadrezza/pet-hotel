from datetime import datetime
from flask import request
from flask_api import status
from flask_jwt_extended import create_access_token, get_current_user
from app.middlewares import api_exception_handler, roles_required
from app.utilities import send_ok, datetime_now, parse_datetime
from app.errors import ErrValidation, ErrInvalidLogin, ErrUserIsBlocked, ErrUserNotFound, ErrEmailAlreadyExist, \
    ErrServiceUnavailable
from .schema import login_request_schema, login_response_schema
from .schema import customer_register_request_schema, customer_register_response_schema
from .schema import create_staff_request_schema, create_staff_response_schema
from .schema import update_status_request_schema
from .schema import get_user_response_schema
from .schema import invite_request_schema
from .service import UserService, CustomerService, StaffService
from .model import UserRole


@api_exception_handler
def login():
    data = request.json
    errors = login_request_schema.validate(data)
    if errors:
        raise ErrValidation(errors)
    email = data["email"]
    password = data["password"]
    user = UserService.get_by_email(email)
    if user is None:
        raise ErrUserNotFound()
    if user.role == UserRole.CUSTOMER and user.is_active is False:
        raise ErrUserIsBlocked()
    if user.check_password(password) is False:
        if user.role == UserRole.CUSTOMER:
            if user.last_failed_login_at == '':
                user.failed_login_attempts = 1
            elif parse_datetime(user.last_failed_login_at).timestamp() + 15 * 60 * 60 < datetime.now().timestamp():
                user.failed_login_attempts = 0
            else:
                user.failed_login_attempts += 1
                if user.failed_login_attempts == 3:
                    user.is_active = False
            user.last_failed_login_at = datetime_now()
            UserService.update(user)
        raise ErrInvalidLogin()
    if user.role == UserRole.CUSTOMER:
        user.failed_login_attempts = 0
        UserService.update(user)
    token = create_access_token(identity=user.dump())
    return send_ok(login_response_schema.dump({"data": {"token": token}}))


@api_exception_handler
@roles_required(['MANAGER', 'STAFF'])
def invite():
    data = request.json
    errors = invite_request_schema.validate(data)
    if errors:
        raise ErrValidation(errors)
    name = data["name"]
    email = data["email"]
    user = UserService.get_by_id(email)
    if user is not None:
        raise ErrEmailAlreadyExist()
    sent = UserService.invite(name, email)
    if sent is False:
        raise ErrServiceUnavailable()
    return send_ok()


@api_exception_handler
def register():
    data = request.json
    errors = customer_register_request_schema.validate(data)
    if errors:
        raise ErrValidation(errors)
    fullname = data["fullname"]
    email = data["email"]
    password = data["password"]
    user = UserService.get_by_email(email)
    if user is not None:
        raise ErrEmailAlreadyExist()
    customer = CustomerService.create(fullname, email, password)
    UserService.insert(customer)
    return send_ok(status_code=status.HTTP_201_CREATED, msg=customer_register_response_schema.dump({"data": customer}))


@api_exception_handler
@roles_required(["MANAGER"])
def create_staff():
    data = request.json
    errors = create_staff_request_schema.validate(data)
    if errors:
        raise ErrValidation(errors)
    fullname = data["fullname"]
    email = data["email"]
    password = data["password"]
    user = UserService.get_by_email(email)
    if user is not None:
        raise ErrEmailAlreadyExist()
    staff = StaffService.create(fullname, email, password)
    UserService.insert(staff)
    return send_ok(status_code=status.HTTP_201_CREATED, msg=create_staff_response_schema.dump({"data": staff}))


@api_exception_handler
@roles_required(["CUSTOMER", "STAFF", "MANAGER"])
def get_user():
    curr_user = get_current_user()
    user = UserService.get_by_id(curr_user.identity)
    if user is None:
        raise ErrUserNotFound()
    return send_ok(get_user_response_schema.dump({"data": user}))


@api_exception_handler
@roles_required(['MANAGER', 'STAFF'])
def update_status(customer_id):
    data = request.json
    errors = update_status_request_schema.validate(data)
    if errors:
        raise ErrValidation(errors)
    active = data["active"]
    user = UserService.get_by_id(customer_id)
    if user is None:
        raise ErrUserNotFound()
    if user.role == UserRole.CUSTOMER:
        user.is_active = active
        UserService.update(user)
    return send_ok()
