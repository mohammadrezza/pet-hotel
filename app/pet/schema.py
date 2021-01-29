from marshmallow import Schema, fields
from marshmallow.validate import Length, OneOf, Range
from .model import PetType


class CreatePetRequestSchema(Schema):
    name = fields.String(required=True, validate=Length(min=3, max=20))
    type = fields.String(required=True, validate=OneOf([x.value for x in PetType.__iter__()]))


class CreatePetResponseSchema(Schema):
    class Pet(Schema):
        identifier = fields.String(required=True)
        name = fields.String(required=True)
        type = fields.String(required=True)

    data = fields.Nested(Pet, required=True)


class EditPetRequestSchema(Schema):
    pet_id = fields.String(required=True)
    name = fields.String(required=True, validate=Length(min=3, max=20))
    type = fields.String(required=True, validate=OneOf([x.value for x in PetType.__iter__()]))
    owner = fields.String(required=False)


class EditPetResponseSchema(Schema):
    class Pet(Schema):
        class Owner(Schema):
            fullname = fields.String(required=True)

        identifier = fields.String(required=True)
        name = fields.String(required=True)
        type = fields.String(required=True)
        room_id = fields.Int(required=True)
        owner = fields.Nested(Owner, required=False)

    data = fields.Nested(Pet, required=True)


class GetPetsRequestSchema(Schema):
    q = fields.String(required=True)
    page = fields.Int(required=True, validate=Range(min=1))
    size = fields.Int(required=True, validate=Range(min=1, max=50))


class GetPetsResponseSchema(Schema):
    class Pet(Schema):
        class Owner(Schema):
            fullname = fields.String(required=True)

        identifier = fields.String(required=True)
        name = fields.String(required=True)
        type = fields.String(required=True)
        room_id = fields.Int(required=True)
        owner = fields.Nested(Owner, required=False)
        created_at = fields.String(required=True)
        updated_at = fields.String(required=True)

    data = fields.List(fields.Nested(Pet), required=True)


class CheckInRequestSchema(Schema):
    room_id = fields.Int(required=True, validate=Range(min=1, max=100))


class MovePetRequestSchema(Schema):
    new_room_id = fields.Int(required=True, validate=Range(min=1, max=100))


create_pet_request_schema = CreatePetRequestSchema()
create_pet_response_schema = CreatePetResponseSchema()
edit_pet_request_schema = EditPetRequestSchema()
edit_pet_response_schema = EditPetResponseSchema()
get_pets_request_schema = GetPetsRequestSchema()
get_pets_response_schema = GetPetsResponseSchema()
check_in_request_schema = CheckInRequestSchema()
move_pet_request_schema = MovePetRequestSchema()
