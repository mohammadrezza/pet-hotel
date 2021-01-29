from marshmallow import Schema, fields
from marshmallow.validate import Length, Email


class LoginRequestSchema(Schema):
    email = fields.String(required=True, validate=Email())
    password = fields.String(required=True, validate=Length(min=8, max=25))


class LoginResponseSchema(Schema):
    class Token(Schema):
        token = fields.String(required=True)

    data = fields.Nested(Token, required=True)


class CustomerRegisterRequestSchema(Schema):
    fullname = fields.String(required=True, validate=Length(min=3))
    email = fields.String(required=True, validate=Email())
    password = fields.String(required=True, validate=Length(min=8, max=25))


class CustomerRegisterResponseSchema(Schema):
    class Customer(Schema):
        identifier = fields.String(required=True)
        fullname = fields.String(required=True)
        email = fields.String(required=True)

    data = fields.Nested(Customer, required=True)


class CreateStaffRequestSchema(Schema):
    fullname = fields.String(required=True, validate=Length(min=3))
    email = fields.String(required=True, validate=Email())
    password = fields.String(required=True, validate=Length(min=8, max=25))


class CreateStaffResponseSchema(Schema):
    class Staff(Schema):
        identifier = fields.String(required=True)
        fullname = fields.String(required=True)
        email = fields.String(required=True)

    data = fields.Nested(Staff, required=True)


class GetUserResponseSchema(Schema):
    class User(Schema):
        identifier = fields.String(required=True)
        fullname = fields.String(required=True)
        email = fields.String(required=True)

    data = fields.Nested(User, required=True)


class InviteRequestSchema(Schema):
    name = fields.String(required=True, validate=Length(min=3))
    email = fields.String(required=True, validate=Email())


class UpdateStatusRequestSchema(Schema):
    active = fields.Boolean(required=True)


login_request_schema = LoginRequestSchema()
login_response_schema = LoginResponseSchema()
customer_register_request_schema = CustomerRegisterRequestSchema()
customer_register_response_schema = CustomerRegisterResponseSchema()
create_staff_request_schema = CreateStaffRequestSchema()
create_staff_response_schema = CreateStaffResponseSchema()
get_user_response_schema = GetUserResponseSchema()
invite_request_schema = InviteRequestSchema()
update_status_request_schema = UpdateStatusRequestSchema()
